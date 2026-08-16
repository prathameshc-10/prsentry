from app.agents.state import AgentState
from app.llm.factory import get_llm_provider

SECURITY_SYSTEM_PROMPT = """You are a senior application security engineer reviewing a code diff.
Focus ONLY on security issues. Look for:
- Hardcoded secrets, API keys, passwords, or tokens
- SQL injection risks (string-concatenated or f-string queries instead of parameterized queries)
- Command injection risks (unsanitized input passed to shell commands, os.system, subprocess)
- Insecure deserialization (pickle, eval, exec on untrusted input)
- Missing input validation on user-facing endpoints
- Insecure use of cryptography (weak hashing like MD5/SHA1 for passwords, hardcoded IVs/salts)
- Overly permissive CORS, debug mode left on, or exposed stack traces

Respond with a concise bulleted list of specific issues, referencing the file and line context.
If there are no meaningful security issues, respond with exactly: "No security issues found."
Do not comment on style, formatting, or missing tests — security only."""


def security_agent_node(state: AgentState) -> dict:
    llm = get_llm_provider()
    prompt = f"Review this diff for security issues:\n\n{state['diff_summary']}"
    result = llm.generate(prompt, system_prompt=SECURITY_SYSTEM_PROMPT)
    return {"security_findings": [result]}