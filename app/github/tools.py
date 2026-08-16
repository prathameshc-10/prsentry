import requests

def post_pr_comment(repo_full_name: str, pr_number: int, token: str, body: str) -> dict:
    """
    Posts a general (issue-style) comment on a PR.
    GitHub treats PR comments as issue comments under the hood.
    """
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"body": body}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()