from datetime import datetime
from app.db.session import SessionLocal
from app.db.models import PullRequest, ReviewRun
from app.github.auth import get_installation_token
from app.github.client import get_pr_files, get_diff_summary
from app.agents.graph import build_graph


def process_pr_review(repo_full_name: str, pr_number: int, run_id: int):
    db = SessionLocal()

    try:
        run = db.query(ReviewRun).filter_by(id=run_id).first()
        run.status = "running"
        run.started_at = datetime.utcnow()
        db.commit()

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
            "security_findings": [],
            "test_findings": [],
            "final_review": "",
        })

        run.status = "completed"
        run.completed_at = datetime.utcnow()
        db.commit()

        print(f"[JOB COMPLETE] {repo_full_name} #{pr_number} — run_id={run.id}")

    except Exception as e:
        db.rollback()
        run.status = "failed"
        run.error_message = str(e)
        run.completed_at = datetime.utcnow()
        db.commit()
        print(f"[JOB FAILED] {repo_full_name} #{pr_number} — {e}")
        raise

    finally:
        db.close()