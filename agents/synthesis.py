from agents.llm_client import call_llm
from prompts.synthesis_prompt import get_synthesis_prompt

def synthesis_agent(topic: str, verified_claims: list) -> str:
    prompt = get_synthesis_prompt(topic, verified_claims)
    draft = call_llm(prompt)
    return draft