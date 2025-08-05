from flask import Flask, request, render_template_string
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from tools import tools
from assistant_output import AssistantOutput
import os

load_dotenv()
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
app = Flask(__name__)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2, google_api_key="GOOGLE_API_KEY")
parser = PydanticOutputParser(pydantic_object=AssistantOutput)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an AI calendar & Email Assistant.
    You help users manage meetings and emails using the available tools.
    Always return a JSON with the following fields:
    -action
    -details
    {format_instructions}
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

chat_history = []

# Minimal HTML interface
HTML_TEMPLATE = """
<!doctype html>
<title>Calendar & Email Assistant</title>
<h2>Ask your assistant</h2>
<form method="post">
  <input name="query" style="width:300px">
  <input type="submit" value="Submit">
</form>
{% if response %}
  <p><strong>Assistant:</strong> {{ response }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        query = request.form["query"]
        chat_history.append(HumanMessage(content=query))
        output = executor.invoke({
            "query": query,
            "chat_history": chat_history
        })
        try:
            structured = parser.parse(output.get("output"))
            chat_history.append(AIMessage(content=structured.details))
            response = structured.details
        except Exception as e:
            response = f"Error parsing output: {e}<br>Raw Output: {output.get('output')}"
    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

