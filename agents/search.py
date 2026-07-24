import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_agent(sub_question:str) -> list:
    response = client.search(query = sub_question, max_results=5)
    results = response.get("results", [])
    return results


