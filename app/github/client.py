import requests

def get_pr_files(repo_full_name: str, pr_number: int, token: str) -> list[dict]:
    """
    Fetch the list of changed files in a PR, including their diffs (patches).
    Returns GitHub's raw file objects: filename, status, additions, deletions, patch, etc.
    """
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_diff_summary(files: list[dict]) -> str:
    """
    Build a single readable diff string from the file list, suitable for feeding to an LLM.
    """
    parts = []
    for f in files:
        filename = f.get("filename")
        patch = f.get("patch", "")  # some files (e.g. binary) won't have a patch
        if patch:
            parts.append(f"### File: {filename}\n{patch}")
    return "\n\n".join(parts)