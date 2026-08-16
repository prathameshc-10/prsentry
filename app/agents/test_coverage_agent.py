from app.agents.state import AgentState
from app.llm.factory import get_llm_provider

TEST_COVERAGE_SYSTEM_PROMPT = """You are a senior engineer reviewing a code diff for test coverage.
Your job is to identify new or modified functions/methods that appear to lack corresponding test coverage.

Look at the diff and determine:
- Are there new functions, methods, or classes with non-trivial logic (branching, calculations, I/O, external calls)?
- Does the diff include any corresponding test file changes (files like test_*.py, *_test.py, or in a tests/ directory)?
- If new logic was added but no test changes appear anywhere in the diff, flag it.

Respond with a concise bulleted list, referencing specific functions/files that need tests.
If the diff includes adequate test changes, or if the changes are trivial (e.g. only config, docs, formatting), respond with exactly: "No test coverage issues found."
Do not comment on style or security — test coverage only."""


def test_coverage_agent_node(state: AgentState) -> dict:
    llm = get_llm_provider()
    prompt = f"Review this diff for test coverage gaps:\n\n{state['diff_summary']}"
    result = llm.generate(prompt, system_prompt=TEST_COVERAGE_SYSTEM_PROMPT)
    return {"test_findings": [result]}