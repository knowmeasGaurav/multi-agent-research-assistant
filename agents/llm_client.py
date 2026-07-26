import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)

def call_llm(prompt: str) -> str:
    response = llm.invoke(prompt)
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