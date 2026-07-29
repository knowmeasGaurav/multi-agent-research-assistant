def get_formatting_prompt(topic: str, draft:str) -> str:
    return f"""You are writing a concise executive summary for a research report on: {topic}

Below is the full narrative draft. Summarize it in 2-3 sentences, capturing the most important takeaways only.

Draft:
{draft}

Respond with only the summary text — no headers, no markdown, no preamble."""