import hmac
import hashlib
import os

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if not signature_header:
        return False
    expected_signature = "sha256=" + hmac.new(
        secret.encode(), payload_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)