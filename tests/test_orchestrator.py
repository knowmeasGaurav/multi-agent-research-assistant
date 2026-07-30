from agents.orchestrator import orchestrator_agent

def test_orchestrator_produces_subquestions():
    result = orchestrator_agent("impact of AI regulation on startups in 2026")

    assert isinstance(result, list)
    assert len(result) >= 3