import sys
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
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a research topic: ")
    final_state = run_pipeline(topic)
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(final_state["final_report"])

    print("\n✅ Report saved to report.md")
    print(f"   Sub-questions researched: {len(final_state['plan'])}")
    print(f"   Claims verified: {len(final_state['verified_claims'])}")