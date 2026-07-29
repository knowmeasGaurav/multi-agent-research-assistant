from agents.verification import verification_agent

def test_verification_flags_contradiction():
    fake_sources = {
        "test question": [
            {"url": "https://example.com/a", "content": "The EU AI Act enters full enforcement in August 2026."},
            {"url": "https://example.org/b", "content": "According to reports, the EU AI Act's full enforcement begins in August 2026."},
            {"url": "https://example.net/c", "content": "Some critics claim the EU AI Act enforcement was delayed to 2027."}
        ]
    }

    result = verification_agent(fake_sources)

    assert len(result) > 0
    assert any(claim["confidence"] == "contradicted" for claim in result)