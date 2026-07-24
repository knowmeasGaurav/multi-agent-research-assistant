# Multi-Agent Research Assistant — Implementation Guide

This is the working build guide — folder structure, dependencies, and step-by-step tasks for each phase. Pair with `ARCHITECTURE.md` for the design rationale.

## Tech stack

- Python 3.11+
- LangChain
- LangGraph
- LLM's API key
- Search: Tavily API (LangChain-native, purpose-built for LLM agents)
- Pydantic (state schema, structured outputs)
- Optional (Phase 8): Streamlit for a demo UI

## Project structure

```
research-assistant/
├── .env                      # API keys (LLM's API KEY, TAVILY_API_KEY)
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── main.py                   # entry point — runs the graph for a given topic
├── state.py                  # shared state schema
├── graph.py                  # LangGraph wiring — nodes + edges
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── search.py
│   ├── verification.py
│   ├── synthesis.py
│   └── formatting.py
├── prompts/
│   ├── orchestrator_prompt.py
│   ├── verification_prompt.py
│   ├── synthesis_prompt.py
│   └── formatting_prompt.py
└── tests/
    ├── test_search.py
    ├── test_orchestrator.py
    ├── test_verification.py
    ├── test_synthesis.py
    └── test_formatting.py
```

Keep prompts in their own files from day one — you'll iterate on them constantly, and it's painful to have prompt text buried inside agent logic.

## requirements.txt

```
langchain
langgraph
langchain-openai
langchain-google-gemini
tavily-python
pydantic
python-dotenv
streamlit          # optional, Phase 8
```

---

## Phase 1 — Skeleton and shared state

**Tasks:**
1. Set up the repo structure above, `.env` with API keys, `requirements.txt`.
2. In `state.py`, define the shared state:
   ```python
   from typing import TypedDict, List, Dict

   class ResearchState(TypedDict):
       topic: str
       plan: List[dict]
       raw_sources: Dict[str, list]
       verified_claims: List[dict]
       draft: str
       final_report: str
   ```
3. In `graph.py`, build the LangGraph `StateGraph(ResearchState)` with five placeholder nodes (`orchestrator_node`, `search_node`, `verification_node`, `synthesis_node`, `formatting_node`) that just return state unchanged.
4. Wire nodes in sequence with `.add_edge(...)`, set entry point, compile the graph.
5. In `main.py`, invoke the graph with a hardcoded topic and print the final state.

**Done when:** running `main.py` executes all five nodes in order without errors and the state object survives the full trip.

---

## Phase 2 — Search agent

**Tasks:**
1. In `agents/search.py`, write a function that takes a sub-question string, calls the Tavily API, returns a list of `{title, url, content}` results.
2. Wire it into `search_node` — iterate over `state["plan"]`, call the search function per sub-question, populate `state["raw_sources"]`.
3. Write `tests/test_search.py` with one hardcoded sub-question, assert non-empty results.

**Done when:** the search node, run standalone with a fake plan, returns real search results into raw_sources.

---

## Phase 3 — Orchestrator agent

**Tasks:**
1. In `prompts/orchestrator_prompt.py`, write the planning prompt: given a topic, produce 3-5 sub-questions covering different angles (recent news, academic/expert view, counterarguments, data/statistics).
2. In `agents/orchestrator.py`, call the Anthropic API with **structured output** (tool calling or a Pydantic output parser) so the plan comes back as parseable JSON, not freeform text — this matters, don't skip it.
3. Wire into `orchestrator_node`, populate `state["plan"]`.
4. Connect orchestrator → search in the graph (already wired in Phase 1, now with real logic on both ends).
5. Write `tests/test_orchestrator.py` — assert the plan is valid JSON with the expected keys and reasonable sub-question count.

**Done when:** `main.py topic="..."` runs orchestrator → search and raw_sources is populated with real per-sub-question results.

---

## Phase 4 — Verification agent

This is the highest-effort phase. Budget the most time here.

**Tasks:**
1. Define your "independent source" rule concretely in `prompts/verification_prompt.py` (e.g. different domains count as independent; syndicated/wire content does not).
2. Prompt the model to extract discrete factual claims from `raw_sources`, then for each claim, identify which sources support it and which contradict it.
3. Force structured output:
   ```python
   class VerifiedClaim(BaseModel):
       claim: str
       supporting_sources: list[str]
       contradicting_sources: list[str]
       confidence: str  # "corroborated" | "contradicted" | "unverified"
   ```
4. Drop claims below a confidence threshold; keep contradicted claims (flagged, not deleted) so they can surface in the report later.
5. Wire into `verification_node`, populate `state["verified_claims"]`.
6. Write `tests/test_verification.py` with a fixture containing two sources that directly contradict each other — assert the agent flags it rather than picking one silently.

**Done when:** feeding the verification agent a fixture with a known contradiction produces a `contradicted` claim, and feeding it a fixture with a single weak/unsupported claim drops it.

---

## Phase 5 — Synthesis agent

**Tasks:**
1. In `agents/synthesis.py`, pass **only** `state["verified_claims"]` into the prompt — do not pass `raw_sources` into this function at all. Enforce this structurally (don't give the function access to the field), not just via prompt instructions.
2. Prompt for narrative synthesis that connects ideas across sub-questions, not a list-per-sub-question summary. Explicitly instruct it to note open questions or flagged contradictions inherited from verification.
3. Wire into `synthesis_node`, populate `state["draft"]`.
4. Write `tests/test_synthesis.py` — feed a small set of verified claims, assert the draft references claims from more than one sub-question in the same paragraph (a proxy for "actual synthesis" vs. listing).

**Done when:** draft text reads as connected prose, not a bulleted source-by-source recap.

---

## Phase 6 — Formatting agent

**Tasks:**
1. In `agents/formatting.py`, split the work: use plain code/templating for structure (headers, citation list), and one LLM call only for the executive summary.
2. Build the final report as Markdown: title, executive summary, body sections, sources list.
3. Wire into `formatting_node`, populate `state["final_report"]`.
4. Write `tests/test_formatting.py` — assert the output contains expected section headers and that every cited source URL actually appears in `verified_claims`.

**Done when:** `state["final_report"]` is a clean, readable Markdown report end to end.

---

## Phase 7 — Integration and edge cases

**Tasks:**
1. Run the full pipeline against 3-5 real, varied topics — not just test fixtures.
2. Handle failure modes explicitly:
   - Search returns zero results for a sub-question → orchestrator or search node should degrade gracefully, not crash.
   - Verification flags everything as unverified → synthesis should say so rather than fabricating a narrative.
   - Contradictory sources with no resolution → make sure this actually surfaces in the final report text.
3. Add state logging at each node (print or write state snapshots to a log file) — useful for debugging and for demoing "here's what each agent did" later.

**Done when:** the pipeline handles a bad-input topic (too narrow, too broad, no search results) without crashing, and you can show a log of what each agent did.

---

## Phase 8 — Polish for portfolio presentation

**Tasks:**
1. Build a minimal Streamlit UI: text input for topic, button to run, spinner while the graph executes, rendered Markdown report at the end.
2. Write `README.md`: what the project is, the architecture diagram, how to run it, stack used. (Your `ARCHITECTURE.md` already has most of this content — link to it or fold it in.)
3. Optional stretch: dynamic re-planning — if verification finds a gap or contradiction the plan didn't anticipate, orchestrator gets re-invoked with the gap as new context and adds a follow-up sub-question.

**Done when:** you can run the Streamlit app, type a topic, and get a polished report — and you have a README good enough to link from your resume/portfolio.

---

## Suggested build order recap

| Phase | Deliverable |
|---|---|
| 1 | Working graph skeleton |
| 2 | Real search results |
| 3 | Real plan → real search |
| 4 | Hallucination-resistant verified claims |
| 5 | Coherent narrative draft |
| 6 | Formatted Markdown report |
| 7 | Robust end-to-end pipeline |
| 8 | Demoable, portfolio-ready project |

**Milestone:** Phase 4 completion is your first genuinely interview-worthy checkpoint — "hallucination-resistant multi-source verification" is a strong, specific thing to talk about even before the project is fully polished.