from fastapi import APIRouter, Request, HTTPException
from app.core.security import verify_signature
from app.jobs.queue import review_queue
from app.jobs.tasks import process_pr_review
from app.db.session import SessionLocal
from app.db.models import PullRequest, ReviewRun
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

        # Create a pending review_run row immediately, before the job even runs
        db = SessionLocal()
        pr_row = db.query(PullRequest).filter_by(
            repo_name=repo_full_name, pr_number=pr_number
        ).first()
        if not pr_row:
            pr_row = PullRequest(repo_name=repo_full_name, pr_number=pr_number)
            db.add(pr_row)
            db.commit()
            db.refresh(pr_row)

        pending_run = ReviewRun(pr_id=pr_row.id, status="pending")
        db.add(pending_run)
        db.commit()
        db.refresh(pending_run)
        run_id = pending_run.id
        db.close()

        # Enqueue the actual work, passing the run_id so the worker updates this exact row
        review_queue.enqueue(process_pr_review, repo_full_name, pr_number, run_id)

        print(f"[JOB ENQUEUED] {repo_full_name} #{pr_number} — run_id={run_id}")

    return {"status": "received"}