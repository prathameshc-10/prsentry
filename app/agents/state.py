from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """"
    Shared state that flows through langgraph pipline.
    Each node reads from and writes to this state.
    """
    repo_full_name: str
    pr_number: int
    installation_token: str

    files_changed: List[Dict[str, Any]]  # raw file objects from GitHub
    diff_summary: str                    # formatted diff text for LLM input

    style_findings: List[str]            # populated by style_agent
    # security_findings, test_findings — will add these Day 3

    final_review: str                    # populated by synthesis step (today: just style output)
