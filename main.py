from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create__tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from tools import tools, draft_email, schedule_event, reschedule_event, cancel_event, read_emails
from assistant_output import AssistantOutput

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

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
  ("human","{query}"),
  ("placeholder", "{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

agent =  create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
executor = AgenticExecutor(agent=agent, tools=tools, verbose=True)

chat_history = []

while True:
  query = input("You: ")
  if query.lower() in ["exit", "quit"]:
    break
  chat_history.append(HumanMessage(content=query))
  response = executor.invoke({
    "query": query,
    "chat_history": chat_history
  })
  try:
    structured = parser.parse(response.get("output"))
    print(f"\n{structured.action}\n{structured.details}")
    chat_history.append(AIMessage(content=structured.details))
  except Exception as e:
    print("\nParsing failed:", e)
    print("Raw:", response.get("output"))
