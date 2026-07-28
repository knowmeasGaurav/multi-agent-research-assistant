from langgraph.graph import StateGraph, END
from state import ResearchState
from agents.orchestrator import orchestrator_agent
from agents.search import search_agent

def orchestrator_node(state: ResearchState) -> ResearchState:
    print("Orchestrator running...")
    sub_questions = orchestrator_agent(state["topic"])
    state["plan"] = sub_questions
    return state

def search_node(state: ResearchState) -> ResearchState:
    print("Search running...")
    raw_sources = {}
    for question in state["plan"]:
        results = search_agent(question)
        raw_sources[question]= results
    
    state["raw_sources"] = raw_sources
    return state

def verification_node(state: ResearchState) -> ResearchState:
    print("Verification running...")
    return state

def synthesis_node(state: ResearchState) -> ResearchState:
    print("Synthesis running...")
    return state

def formatting_node(state: ResearchState) -> ResearchState:
    print("Formatting running...")
    return state


graph = StateGraph(ResearchState)

graph.add_node("orchestrator", orchestrator_node)
graph.add_node("search", search_node)
graph.add_node("verification", verification_node)
graph.add_node("synthesis", synthesis_node)
graph.add_node("formatting", formatting_node)

graph.set_entry_point("orchestrator")

graph.add_edge("orchestrator","search")
graph.add_edge("search", "verification")
graph.add_edge("verification", "synthesis")
graph.add_edge("synthesis", "formatting")
graph.add_edge("formatting", END)

compiled_graph = graph.compile()