from app.agents.state import AgentState
from app.llm.factory import get_llm_provider

STYLE_SYSTEM_PROMPT = """You are a senior code reviewer focused ONLY on code style and readability.
Review the given diff and identify style issues: naming conventions, formatting inconsistencies,
missing docstrings/comments, overly complex lines, dead code, or anti-patterns.

Respond with a concise bulleted list of specific issues, referencing the file and line context.
If there are no meaningful style issues, respond with exactly: "No style issues found."
Do not comment on functionality, security, or logic — style only."""


def style_agent_node(state: AgentState) -> AgentState:
    llm = get_llm_provider()

    prompt = f"Review this diff for style issues:\n\n{state['diff_summary']}"
    result = llm.generate(prompt, system_prompt=STYLE_SYSTEM_PROMPT)

    state["style_findings"] = [result]
    state["final_review"] = result  # today: style output IS the final review

    return state