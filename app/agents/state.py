from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    """
    Shared state that flows through the LangGraph pipeline.
    Each node reads from and writes to this state.
    """
    repo_full_name: str
    pr_number: int
    installation_token: str

    files_changed: List[Dict[str, Any]]   # raw file objects from GitHub
    diff_summary: str                      # formatted diff text for LLM input

    style_findings: List[str]              # populated by style_agent
    security_findings: List[str]           # populated by security_agent
    test_findings: List[str]               # populated by test_coverage_agent

    final_review: str                      # populated by synthesis_agent