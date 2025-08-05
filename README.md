# Calender_&_Email_assistant

A conversational assistant that helps users manage meetings and emails using natural language commands. Built using LangChain, Gemini (Google AI), and custom tool integrations, this assistant supports scheduling, rescheduling, cancelling events, reading emails, and drafting replies — all through a simple terminal interface.

# 🚀 Features
✅ Conversational interface in terminal
📅 Schedule, reschedule, or cancel events using natural language
📧 Read emails and draft replies automatically
🧠 Uses Google Gemini (gemini-2.5-flash) via LangChain
🛠 Modular tools system for calendar & email control
🔐 Environment-based API key management

# Tech Stack
1. LangChain (Agent logic & tool integration)
2. Gemini (Google AI)	(LLM for understanding and response)
3. Python	(Core backend)
4. Replit	(Cloud IDE & deployment)
5. dotenv / Secrets	(Secure API key handling)

# Live Demo (Replit)
try the assistant live on replit: 
https://replit.com/@dpkaru10/CalenderandEmailassistant

# Environment Variables
GOOGLE_API_KEY- Required. Gemini API key from Google AI Studio

# Setup Instructions
1. Clone the repo
   git clone https://github.com/yourusername/Calender_and_Email_assistant
2. Install dependencies
   pip install -r requirements.txt
3. Set your Gemini API key
   Option A: Use .env (only for local)
     GOOGLE_API_KEY=your_real_key_here
   Option B: Replit Secrets
     Key: GOOGLE_API_KEY
     Value: (your Gemini API key)
4. Run the assistant
   python main.py
5. Interact
   You: Schedule a meeting tomorrow at 5 PM with Alex
   You: Read the latest email
   You: Quit

# Example Prompts 
1. "Schedule a meeting called 'Team Trio' tomorrow at 11 AM"
2. "Reschedule my 2 PM doctor appointment to 3 PM"
3.  "Cancel the dentist appointment at 4 PM"
4.  "Read my latest emails"
5.  "Draft a reply to John saying I’m available"
