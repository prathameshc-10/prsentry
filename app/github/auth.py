import jwt
import time
import os
import requests

def generate_jwt() -> str:
    """
    Generate a short-lived JWT signed with the GitHub App's private key.
    GitHub uses this JWT to verify we ARE the app we claim to be.
    """
    app_id = os.getenv("GITHUB_APP_ID")
    private_key_path = os.getenv("GITHUB_PRIVATE_KEY_PATH")

    with open(private_key_path, "r") as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        'iat': now - 60,         # issued at (60s in the past to allow for clock drift)
        'exp': now + (9 * 60),   # expires in 9 minutes (GitHub max is 10)
        'iss': app_id,           # issuer = our App ID
    }

    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_token() -> str:
    """
    Exchange the app-level JWT for a short-lived (1hr) installation access token.
    This token is what actually lets us call GitHub's API as the app,
    scoped only to the repos this installation has access to.
    """
    installation_id = os.getenv("GITHUB_INSTALLATION_ID")
    app_jwt = generate_jwt()

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    headers = {
        "Authorization": f"Bearer {app_jwt}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    return response.json()["token"]