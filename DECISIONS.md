- Used GitHub App (not PAT) for scoped, installable auth
- Webhook signature verified via HMAC-SHA256 against X-Hub-Signature-256
- smee.io used for local webhook forwarding during dev (would use a real 
  deployed endpoint in production)