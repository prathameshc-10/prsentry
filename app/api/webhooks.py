from fastapi import APIRouter, Request, HTTPException
from app.core.security import verify_signature
from app.github.auth import get_installation_token
from app.github.client import get_pr_files, get_diff_summary
from app.agents.graph import build_graph
import json

router = APIRouter()

@router.post("/webhooks/github")
async def github_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body)
    event_type = request.headers.get("X-GitHub-Event")
    action = payload.get("action")

    if event_type == "pull_request" and action in ("opened", "synchronize"):
        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]
        print(f"[PR EVENT] {repo_full_name} #{pr_number} — action: {action}")

        # Trigger the review pipeline
        token = get_installation_token()
        files = get_pr_files(repo_full_name, pr_number, token)
        diff = get_diff_summary(files)

        graph = build_graph()
        graph.invoke({
            "repo_full_name": repo_full_name,
            "pr_number": pr_number,
            "installation_token": token,
            "files_changed": files,
            "diff_summary": diff,
            "style_findings": [],
            "final_review": "",
        })

        print(f"[REVIEW POSTED] {repo_full_name} #{pr_number}")

    return {"status": "received"}