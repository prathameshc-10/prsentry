from dotenv import load_dotenv
load_dotenv()

from app.github.auth import get_installation_token
from app.github.client import get_pr_files, get_diff_summary
from app.agents.security_agent import security_agent_node

token = get_installation_token()
files = get_pr_files("prathameshc-10/prsentry-testbed", 3, token)  # PR #2 from yesterday
diff = get_diff_summary(files)

state = {
    "repo_full_name": "prathameshc-10/prsentry-testbed",
    "pr_number": 2,
    "installation_token": token,
    "files_changed": files,
    "diff_summary": diff,
    "style_findings": [],
    "security_findings": [],
    "test_findings": [],
    "final_review": "",
}

result = security_agent_node(state)
print("=== SECURITY FINDINGS ===")
print(result["security_findings"][0])