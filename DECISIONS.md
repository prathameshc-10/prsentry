# PRSentry — Design Decisions Log

A running log of architecture and design decisions made during the build, with the reasoning behind each one. Kept short and dated — meant to be a quick reference for interviews and future-me.

---

## Day 1 — Foundation & Webhook Infra

**Decision: Used a GitHub App, not a Personal Access Token (PAT)**
- A PAT is tied to a personal account, has broad/unscoped access, and doesn't expire on its own.
- A GitHub App is installable per-repo, gets fine-grained permissions (only Pull requests + Contents read/write, not full repo access), and authenticates via short-lived (1hr) installation tokens generated from a JWT + private key.
- This is how real production bots (Dependabot, CodeRabbit, etc.) authenticate — it's a meaningfully more production-grade choice than a hardcoded token.

**Decision: Verified webhook signatures with HMAC-SHA256**
- GitHub signs every webhook payload with a shared secret (`X-Hub-Signature-256` header).
- Implemented `verify_signature()` in `app/core/security.py` using `hmac.compare_digest` (constant-time comparison, avoids timing attacks) rather than a plain `==` check.
- Without this, anyone could POST a fake payload to the webhook endpoint and trigger the agent — this closes that hole.

**Decision: Used smee.io for local webhook forwarding during development**
- GitHub can't deliver webhooks to `localhost` directly, since it needs a publicly reachable HTTPS URL.
- smee.io provides a persistent public URL that forwards events to a local port over a websocket connection — GitHub only ever talks to smee.io's valid HTTPS endpoint, so "Enable SSL verification" stays on safely.
- This is a dev-only tool. In production, PRSentry would be deployed behind a real HTTPS endpoint (e.g. a cloud-hosted FastAPI service) and the GitHub App's webhook URL would point there directly — smee would be removed entirely.

**Decision: FastAPI for the webhook receiver**
- Async-native, which matters since webhook handling should return fast (200 OK) and hand off real processing to a background job/queue rather than blocking the request — this groundwork is set up for Day 4 (Redis/Celery async processing).

**Verified end-to-end today:**
GitHub → GitHub App → smee.io → local FastAPI (`/webhooks/github`) → signature verified → payload parsed → PR number/repo logged → `200 OK` returned.

---

## Open items / things to revisit
- Webhook secret was generated via `openssl rand -hex 20`; should be rotated before any public/production use since it appeared in local screenshots during setup.
- `.pem` private key and `.env` are gitignored — confirm before first commit that neither is accidentally staged.