from fastapi import APIRouter, Request, HTTPException
from app.core.security import verify_signature
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
        repo_name = payload["repository"]["full_name"]
        print(f"[PR EVENT] {repo_name} #{pr_number} — action: {action}")

    return {"status": "received"}