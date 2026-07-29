def get_verification_prompt(raw_sources: dict) -> str:
    sources_text = ""
    for question, results in raw_sources.items():
        sources_text += f"\n\nSub-question: {question}\n"
        for i, r in enumerate(results):
            sources_text += f"  Source {i+1} ({r.get('url')}): {r.get('content', '')[:500]}\n"

    return f"""You are a fact-verification agent. Below are search results grouped by sub-question.

Your job:
1. Extract concrete factual claims from the sources.
2. For each claim, identify which sources support it and which contradict it.
3. Two sources only count as independent if they have different domains (e.g. reuters.com and apnews.com are independent; two articles both on reuters.com are not).
4. Drop claims that are clearly just ads, navigation text, or irrelevant to the sub-question.

Apply these confidence rules exactly — do not use judgment beyond them:
- "corroborated": 2+ independent sources support the claim, AND zero sources contradict it
- "contradicted": at least 1 source directly conflicts with at least 1 other source on this claim
- "unverified": only 1 source mentions the claim, or support is vague/indirect

{sources_text}

Respond ONLY with a JSON array of objects, each shaped exactly like this:
{{"claim": "...", "supporting_sources": ["url1", "url2"], "contradicting_sources": [], "confidence": "corroborated", "reasoning": "one sentence explaining the classification"}}

No other text, no markdown formatting, no explanation outside the JSON — JSON array only."""