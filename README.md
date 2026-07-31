# Multi-Agent Research Assistant

Give it a topic, and instead of one LLM call generating a generic essay, multiple specialized agents work together — search, verify, synthesize, and format — to produce a research report grounded in cross-checked sources.

This mirrors the orchestration patterns real production AI research tools use (e.g. Perplexity), rather than the "call the LLM once" pattern most tutorials stop at.

## Status

✅ Complete — all 5 agents built, tested, and wired end-to-end. Includes a Streamlit UI, retry/backoff for rate limits, and error handling for malformed LLM output and failed searches.

**Live demo:** [ https://multiagent-research-assistant-project.streamlit.app/ ]

## How it works

1. **Orchestrator agent** — breaks the topic into targeted sub-questions
2. **Search agent** — fetches raw sources per sub-question
3. **Verification agent** — cross-checks claims across sources, flags contradictions, discards weak sources
4. **Synthesis agent** — writes a coherent narrative from verified claims
5. **Formatting agent** — structures the narrative into a final report

All agents read/write a shared state object passed through a LangGraph pipeline.

See [`docs/ProjectArchitecture.md`](docs/ProjectArchitecture.md) for full architecture details.

## Stack

- Python
- LangChain + LangGraph
- Google Gemini API
- Tavily (search)
- Streamlit (UI)
- uv (package/environment management)

## Setup

```bash
uv sync
```

Create a `.env` file with:
```
GOOGLE_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

## Run

Streamlit UI:
```bash
uv run python -m streamlit run app.py
```

Or run the pipeline directly via CLI:
```bash
uv run python main.py "your research topic"
```

## Tests

```bash
uv run pytest
```

Note: `test_orchestrator.py` and `test_search.py` make real API calls (Gemini/Tavily). The rest use fake fixture data and don't consume API quota.