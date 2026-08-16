from dotenv import load_dotenv
load_dotenv()

from app.github.auth import get_installation_token
import requests

token = get_installation_token()
print("Got token:", token[:20] + "...")  # don't print the full token

# Sanity check: fetch repo info using this token
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
}
resp = requests.get("https://api.github.com/repos/prathameshc-10/prsentry-testbed", headers=headers)
print(resp.status_code)
print(resp.json().get("full_name"))