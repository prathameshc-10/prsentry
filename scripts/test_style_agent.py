from dotenv import load_dotenv
load_dotenv()

from app.github.auth import get_installation_token
from app.github.client import get_pr_files, get_diff_summary
from app.agents.graph import build_graph

token = get_installation_token()
files = get_pr_files("prathameshc-10/prsentry-testbed", 1, token)
diff = get_diff_summary(files)

graph = build_graph()
result = graph.invoke({
    "repo_full_name": "prathameshc-10/prsentry-testbed",
    "pr_number": 1,
    "installation_token": token,
    "files_changed": files,
    "diff_summary": diff,
    "style_findings": [],
    "final_review": "",
})

print("=== FINAL REVIEW ===")
print(result["final_review"])