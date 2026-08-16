from dotenv import load_dotenv
load_dotenv()

from app.github.auth import get_installation_token
from app.github.client import get_pr_files, get_diff_summary
from app.agents.style_agent import style_agent_node
from app.agents.security_agent import security_agent_node
from app.agents.test_coverage_agent import test_coverage_agent_node
from app.agents.synthesis_agent import synthesis_agent_node

token = get_installation_token()
files = get_pr_files("prathameshc-10/prsentry-testbed", 3, token)
diff = get_diff_summary(files)

state = {
    "repo_full_name": "prathameshc-10/prsentry-testbed",
    "pr_number": 3,
    "installation_token": token,
    "files_changed": files,
    "diff_summary": diff,
    "style_findings": [],
    "security_findings": [],
    "test_findings": [],
    "final_review": "",
}

state = style_agent_node(state)
state = security_agent_node(state)
state = test_coverage_agent_node(state)
state = synthesis_agent_node(state)

print("=== FINAL SYNTHESIZED REVIEW ===")
print(state["final_review"])