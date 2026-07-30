import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

def call_llm(prompt: str, max_retries: int = 3) -> str:
    response = None
    
    for attempt in range(max_retries):
        try:
            response = llm.invoke(prompt)
            break
        except Exception as e:
            is_rate_limit = "RESOURCE_EXHAUSTED" in str(e)
            if is_rate_limit and attempt < max_retries -1:
                wait_time = 60
                print(f"Rate limit hit. Waiting {wait_time}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise

    
    raw_text = response.content

    if isinstance(raw_text, list):
        raw_text = "".join(
            part["text"] if isinstance(part, dict) else str(part)
            for part in raw_text
        )

    raw_text = raw_text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").replace("json", "", 1).strip()

    return raw_text