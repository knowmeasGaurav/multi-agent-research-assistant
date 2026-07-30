import json
from agents.llm_client import call_llm
from prompts.verification_prompt import get_verification_prompt

def verification_agent(raw_sources: dict) -> list:
    prompt = get_verification_prompt(raw_sources)
    raw_text = call_llm(prompt)

    try:
        verified_claims = json.loads(raw_text)
    except json.JSONDecodeError:
        print("Verification: failed to parse claims, returning empty claim list.")
        verified_claims = []

    return verified_claims