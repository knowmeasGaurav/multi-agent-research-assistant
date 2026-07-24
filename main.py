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
    result = search_agent("latest ai regulation news 2026")
    for r in result:
        print(r.get("title"),"-",r.get("url"))