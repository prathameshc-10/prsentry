from dotenv import load_dotenv
load_dotenv()

from app.github.auth import get_installation_token
from app.github.client import get_pr_files, get_diff_summary

token = get_installation_token()
files = get_pr_files("prathameshc-10/prsentry-testbed", 1, token)

print(f"Files changed: {len(files)}")
for f in files:
    print("-", f["filename"], f"(+{f['additions']}/-{f['deletions']})")

print("\n--- DIFF SUMMARY ---\n")
print(get_diff_summary(files))