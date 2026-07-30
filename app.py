import streamlit as st
from graph import compiled_graph

st.set_page_config(page_title="Multi-Agent Research Assistant", layout="centered")
st.title("Multi-Agent Research Assistant")
st.write("Give it a topic — multiple agents will search, verify, and synthesize a report.")

topic = st.text_input("Research topic", placeholder="e.g. impact of AI regulation on startups in 2026")
run_button = st.button("Run Research", type="primary")

if run_button and topic:
    status_placeholder = st.empty()
    progress_steps = ["Orchestrator", "Search", "Verification", "Synthesis", "Formatting"]

    initial_state = {
        "topic": topic,
        "plan": [],
        "raw_sources": {},
        "verified_claims": [],
        "draft": "",
        "final_report": ""
    }

    with st.spinner("Running pipeline..."):
        for step in progress_steps:
            status_placeholder.info(f"🔄 {step} running...")

        final_state = compiled_graph.invoke(initial_state)

    status_placeholder.success("✅ Report complete!")

    st.subheader("Sub-questions researched")
    for q in final_state["plan"]:
        st.write(f"- {q}")

    st.subheader("Final Report")
    st.markdown(final_state["final_report"])

    st.download_button(
        "Download report.md",
        data=final_state["final_report"],
        file_name="report.md",
        mime="text/markdown"
    )