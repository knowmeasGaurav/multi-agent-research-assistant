from agents.synthesis import synthesis_agent

def test_synthesis_produces_narrative():
    fake_claims = [
        {"claim": "The EU AI Act enters full enforcement in August 2026.", "confidence": "corroborated", "reasoning": "Two independent sources agree."},
        {"claim": "AI startups received over half of total VC investment in 2026.", "confidence": "corroborated", "reasoning": "Three independent sources agree."}
    ]
    draft = synthesis_agent("impact of AI regulation on startups in 2026", fake_claims)

    assert isinstance(draft, str)
    assert len(draft) > 100