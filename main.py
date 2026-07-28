from graph import compiled_graph
from agents.search import search_agent

def run_pipeline(topic: str):
    initial_state = {
        "topic": topic,
        "plan": [],
        "raw_sources": {},
        "verified_claims": [],
        "draft": "",
        "final_report": ""
    }

    result = compiled_graph.invoke(initial_state)
    return result

if __name__ == "__main__":
    topic = "impact of AI regulation on startups in 2026"
    final_state = run_pipeline(topic)
    print("\nFinal state:")
    print(final_state)