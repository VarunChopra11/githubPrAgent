import requests

def get_pr_changes(repo_url: str, pr_number: int, github_token: str = None) -> str:
    """
    Get the changes made in a pull request.
    """
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Extract the repository name from the URL
    repo = repo_url.replace("https://github.com/", "").rstrip("/")

    # Get list of files changed in the pull request
    pr_files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"

    # Handling whether a GitHub token is provided or not
    if not github_token:
        response = requests.get(pr_files_url)
    else:
        response = requests.get(pr_files_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve files: {response.json().get('message', 'Unknown error')}")

    # Process files and build the output string with changes
    files = response.json()
    pr_changes = ""
    
    for file in files:
        file_path = file['filename']
        patch = file.get('patch', '')  # Default to empty string if 'patch' is missing
        pr_changes += f"File: {file_path}\nChanges:\n{patch}\n\n"
    return pr_changes