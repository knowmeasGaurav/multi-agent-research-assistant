from agents.llm_client import call_llm
from prompts.formatting_prompt import get_formatting_prompt

def formatting_agent(topic: str, draft:str, verified_claim:list)-> str:
    prompt = get_formatting_prompt(topic, draft)
    summary = call_llm(prompt)

    sources = set()
    for claim in verified_claim:
        sources.update(claim.get("supporting_sources", []))
        sources.update(claim.get("contradicting_sources", []))

    sources_list = "\n".join(f"-{url}" for url in sorted(sources))

    report = f"""# Research Report: {topic}

## Executive Summary
{summary}

## Findings
{draft}

## Sources
{sources_list}
"""
    return report
        