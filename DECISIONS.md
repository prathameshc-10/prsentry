# PRSentry — Design Decisions Log

A running log of architecture and design decisions made during the build, with the reasoning behind each one. Kept short and dated — meant to be a quick reference for interviews and future-me.

---

## Day 1 — Foundation & Webhook Infra

**Decision: Used a GitHub App, not a Personal Access Token (PAT)**
- A PAT is tied to a personal account, has broad/unscoped access, and doesn't expire on its own.
- A GitHub App is installable per-repo, gets fine-grained permissions (only Pull requests + Contents read/write, not full repo access), and authenticates via short-lived (1hr) installation tokens generated from a JWT + private key (see Day 2 for the implementation).
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

## Day 2 — Diff Fetching, LLM Review Agent, Autonomous Posting

**Decision: GitHub App JWT → Installation Token flow implemented and verified**
- JWT (app-level identity) exchanged for a short-lived (1hr) installation token
  scoped to actual repo permissions — confirmed working via direct API call.

**Decision: Pluggable LLM provider via abstract base class + factory pattern**
- `LLMProvider` ABC with `generate()` method; `GeminiProvider` implemented first.
- Provider selected via `LLM_PROVIDER` env var — switching to Ollama/OpenAI later
  requires zero changes to agent code, only a new provider class + env value.
- Chose this now (not after building more agents) since retrofitting an abstraction
  after multiple agents depend on a hardcoded LLM call is expensive to undo.

**Decision: Migrated to `google-genai` SDK immediately upon deprecation warning**
- Old `google-generativeai` package is fully sunset by Google; fixed in ~5 min
  rather than letting technical debt accumulate on a package with no future updates.

**Decision: LangGraph pipeline currently linear (style_agent → post_review → END)**
- Single-node graph today; Day 3 will fan this out to parallel security/test-coverage
  agents feeding into a synthesis node before posting — current structure is designed
  to extend cleanly (AgentState already has room for more finding fields).

**Decision: Webhook currently processes synchronously (blocking)**
- Acceptable for now since Gemini Flash responds fast enough to stay under GitHub's
  webhook timeout, but this is a known limitation — Day 4 moves this to an async
  Redis job queue so webhook response isn't coupled to LLM latency.

**Fixed: Default branch was `test-pr-1`, not `main`**
- Since `test-pr-1` was the first branch ever pushed to the empty testbed repo,
  GitHub set it as default. Corrected via repo Settings → Default branch → `main`.

**Verified end-to-end today:**
Real PR pushed → webhook fires → diff fetched via GitHub API → Gemini 2.5 Flash
reviews it → posted autonomously as a PR comment by the GitHub App bot account,
zero manual steps.

**Result:** Style agent caught 14 distinct issues on a test file (unused imports,
naming convention violations, missing docstrings, semicolon-chained statements,
missing trailing newline) — all with accurate line numbers, in a single LLM call.

---

## Open items / things to revisit
- Webhook processing is synchronous — move to async Redis job queue (planned Day 4).
- LangGraph pipeline is single-node — expand to parallel security/test-coverage agents + synthesis node (planned Day 3).