# Multi-Agent Research Assistant — Architecture

## What it does

Given a topic (e.g. "impact of AI regulation on startups in 2026"), the system uses multiple specialized agents — rather than one LLM call — to search, verify, synthesize, and format a research report. Each agent has a narrow job and passes its work to the next via shared state.

This mirrors production orchestration patterns used by real AI research tools (Perplexity, AutoGPT-style tools, enterprise research assistants), rather than the "call the LLM once" pattern most tutorials stop at.

## Pipeline overview

```
Topic
  │
  ▼
┌─────────────────────┐
│  Orchestrator agent  │  Breaks topic into sub-questions, assigns agents
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│    Search agent      │  Fetches raw sources per sub-question (no analysis)
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  Verification agent  │  Cross-checks claims, flags contradictions,
│                       │  discards weak sources
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│   Synthesis agent     │  Writes coherent narrative from verified claims
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  Formatting agent     │  Builds final report (headers, citations, summary)
└─────────┬────────────┘
          ▼
     Final report
```

All agents read from and write to one **shared state object** passed along the pipeline — this is what makes it a coordinated system rather than five disconnected LLM calls.

## Agent details

### 1. Orchestrator agent
- **Input:** raw topic string
- **Output:** structured plan (list of sub-questions, each tagged with the agent to handle it)
- One LLM call, structured/JSON output — not freeform text — so the rest of the pipeline can iterate over it programmatically.
- Design decision: static one-shot plan (simpler, build first) vs. dynamic re-planning if verification finds a gap (advanced upgrade, later).

### 2. Search agent
- **Input:** one sub-question at a time
- **Output:** raw search results (titles, snippets, URLs, possibly full text)
- Deliberately mechanical — no LLM reasoning, just a search API call (e.g. Tavily, Serper, Bing API). Keeps this stage cheap, fast, and independently swappable.

### 3. Verification agent
- **Input:** raw search results across all sub-questions
- **Output:** cleaned claims, each tagged corroborated / contradicted / unverified, weak sources dropped
- The most LLM-intensive, most important stage — this is what prevents hallucinated "facts" from reaching the report.
- Needs a concrete rule for "independent" sources (e.g. syndicated wire articles don't count as two confirmations).
- Contradictions are flagged, not silently discarded — they can surface in the final report as "sources disagree on X."

### 4. Synthesis agent
- **Input:** verified claims only — never raw/unverified sources
- **Output:** coherent narrative draft
- Job is to connect ideas across sub-questions, not list facts per sub-question — that's what makes it synthesis rather than summary.

### 5. Formatting agent
- **Input:** synthesized narrative
- **Output:** final structured report (headers, executive summary, citations)
- Should be close to deterministic — no new claims introduced here. Could be mostly templating/code, with the LLM used only for the executive summary.

## Shared state schema

```python
class ResearchState(TypedDict):
    topic: str
    plan: list[dict]              # sub-questions + assigned agent
    raw_sources: dict[str, list]  # sub_question -> [search results]
    verified_claims: list[dict]   # {claim, supporting_sources, contradicting_sources, confidence}
    draft: str
    final_report: str
```

Each agent reads only the fields it needs and writes only the fields it owns. In LangGraph, this maps directly onto the graph's state schema — each agent is a node, edges are the orchestrator's plan.

## Implementation plan (phase-wise)

| Phase | Focus | Goal |
|---|---|---|
| 1 | Skeleton & shared state | Define state schema, wire up 5 placeholder LangGraph nodes that pass state through unchanged |
| 2 | Search agent | Real search API call, no LLM, test in isolation |
| 3 | Orchestrator agent | Structured planning LLM call, connect to search agent |
| 4 | Verification agent | Claim extraction + cross-source corroboration logic; test against a known contradiction |
| 5 | Synthesis agent | Narrative generation from verified claims only (enforced in code, not just prompt) |
| 6 | Formatting agent | Templating + LLM-generated executive summary |
| 7 | Integration & edge cases | Full end-to-end runs, handle empty search results, all-unverified claims, unresolved contradictions, add state logging |
| 8 | Polish | CLI or Streamlit UI, README, optional: dynamic re-planning |

**Milestone:** after Phase 4, you already have a defensible "hallucination-resistant research pipeline" — Phases 5–8 turn it into a polished, demoable project.

## Stack

- Python
- LangChain
- LangGraph
- LLM's API