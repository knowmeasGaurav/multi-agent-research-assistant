def get_synthesis_prompt(topic: str, verified_claims: list)->str:
    claims_text = ""
    for c in verified_claims:
        claims_text += f"\n- Claims: {c.get('claim')}\n Confidence: {c.get('Confidence')}\n Reasoning: {c.get('reasoning')}\n"

    return f"""You are a research synthesis agent writing about: {topic}

Below are verified claims, each with a confidence level (corroborated, contradicted, or unverified).

{claims_text}

Write a coherent narrative that:
1. Connects ideas across claims rather than listing them one by one.
2. Clearly notes where sources disagree ("contradicted" claims) instead of picking a side.
3. Treats "unverified" claims as tentative — flag them as such, don't state them as fact.
4. Does not introduce any claim, fact, or number that isn't in the list above.

Write 3-5 paragraphs of plain prose. No headers, no bullet points, no markdown — just narrative text."""
