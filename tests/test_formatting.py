from agents.formatting import formatting_agent

def test_formatting_produces_report():
    fake_claims = [
        {"claim": "Test claim", "supporting_sources": ["https://a.com"], "contradicting_sources": [], "confidence": "corroborated"}
    ]
    report = formatting_agent("test topic", "This is a test draft narrative.", fake_claims)

    assert "# Research Report" in report
    assert "https://a.com" in report