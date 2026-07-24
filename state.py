from typing import TypedDict, List, Dict

class ResearchState(TypedDict):
    topic: str
    plan: List[dict]
    raw_sources: Dict[str, List]
    verified_claims: List[dict]
    draft: str
    final_report: str
