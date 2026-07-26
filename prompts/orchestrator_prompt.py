def get_orchestrator_prompt(topic:str)->str:
    return f"""You are a Research planning agent
    Given a research topic, break it into 3-5 specific, independently-searchable sub-questions that cover different angles: recent developments, expert/academic opinion, counterarguments, and relevant data or statistics.

Topic: {topic}

Respond ONLY with a JSON array of strings, one sub-question per element. No other text, no markdown formatting."""