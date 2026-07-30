import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.orchestrator_prompt import get_orchestrator_prompt
from agents.llm_client import call_llm

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def orchestrator_agent(topic:str)->list:
    prompt= get_orchestrator_prompt(topic)
    raw_text = call_llm(prompt)
    
    sub_questions = json.loads(raw_text)
    return sub_questions
