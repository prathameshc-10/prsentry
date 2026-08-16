from app.agents.state import AgentState
from app.llm.factory import get_llm_provider

SYNTHESIS_SYSTEM_PROMPT = """You are a senior engineering lead compiling a final code review from three
specialist reviews: style, security, and test coverage.

Your job:
1. Merge the three inputs into ONE clean, well-organized review.
2. Group findings under clear headers: "🔒 Security", "🧪 Test Coverage", "🎨 Style & Readability"
3. Within each section, order findings by severity (most important first). Security issues are
   always the highest priority overall — if there are security findings, note that at the top.
4. Remove any duplicate or overlapping points across sections.
5. Keep it concise — use bullet points, reference file:line where available, no fluff or repeated
   preambles like "Here are the findings".
6. If a section has no findings, omit that section entirely rather than writing "None found".
7. End with a one-line overall summary sentence (e.g. "3 security issues should be addressed before merging.")

Do not invent new findings — only reorganize and summarize what's given to you."""


def synthesis_agent_node(state: AgentState) -> dict:
    llm = get_llm_provider()
    combined_input = f"""STYLE FINDINGS:
{state['style_findings'][0] if state['style_findings'] else 'None'}

SECURITY FINDINGS:
{state['security_findings'][0] if state['security_findings'] else 'None'}

TEST COVERAGE FINDINGS:
{state['test_findings'][0] if state['test_findings'] else 'None'}"""

    result = llm.generate(combined_input, system_prompt=SYNTHESIS_SYSTEM_PROMPT)
    return {"final_review": result}