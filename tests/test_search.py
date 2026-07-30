from agents.search import search_agent

def test_search_returns_results():
    results = search_agent("latest AI regulation news 2026")

    assert isinstance(results, list)
    assert len(results) > 0