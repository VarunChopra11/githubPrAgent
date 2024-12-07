import re
import json
import requests
from app.config import Config

def generate_prompt(pr_changes: str) -> str:
    """
    Generate a prompt for the AI agent to analyze the code changes in a pull request.
    """

    return (
        "You are a code review assistant. Analyze the following code changes in the pull request. For each file, identify the following issues:\n"
        "1. **Code style issues** (e.g., line length, indentation, naming conventions).\n"
        "2. **Bugs or potential errors** (e.g., null pointer dereferencing, incorrect logic).\n"
        "3. **Performance issues** (e.g., inefficient loops, redundant operations).\n"
        "4. **Best practices** (e.g., missing documentation, unnecessary complexity).\n\n"
        "For each identified issue, provide the following details in JSON format:\n"
        "- **type**: The type of issue (e.g., style, bug, performance, best practice).\n"
        "- **line**: The line number where the issue is found.\n"
        "- **description**: A brief description of the issue.\n"
        "- **suggestion**: A suggestion for improving the code.\n\n"
        "Return only the JSON response in the format below. Do not include any additional text or explanations.\n\n"
        "Example format:\n"
        '"results": {\n'
        '    "files": [\n'
        '        {\n'
        '            "name": "main.py",\n'
        '            "issues": [\n'
        '                {\n'
        '                    "type": "style",\n'
        '                    "line": 15,\n'
        '                    "description": "Line too long",\n'
        '                    "suggestion": "Break line into multiple lines"\n'
        '                },\n'
        '                {\n'
        '                    "type": "bug",\n'
        '                    "line": 23,\n'
        '                    "description": "Potential null pointer",\n'
        '                    "suggestion": "Add null check"\n'
        '                }\n'
        '            ]\n'
        '        }\n'
        '    ],\n'
        '    "summary": {\n'
        '        "total_files": 1,\n'
        '        "total_issues": 2,\n'
        '        "critical_issues": 1\n'
        '    }\n'
        '}}\n\n'
        "Now analyze the following changes:\n\n"
        f"{pr_changes}"
    )

def parse_json_response(response_text):
    """
    Parse the Text Response from the AI agent to Json.
    """

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass
    return None

def generate_response_from_agent(changes: str) -> dict:
    """
    Generate a code review response from the AI agent.
    """
    headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_API_KEY,
    }

    prompt = generate_prompt(changes)

    data = {
        "messages": [
            {"role": "system", "content": "You are an Expert code analyzer."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
    }
    params = {"api-version": Config.AZURE_API_VERSION}

    try:
        response = requests.post(Config.AZURE_ENDPOINT, headers=headers, json=data, params=params)
        response.raise_for_status()
        result_text = response.json()["choices"][0]["message"]["content"]
        json_parsed_response = parse_json_response(result_text)
        json_to_string_response = json.dumps(json_parsed_response, indent=4)
        return {
            "status": "success",
            "response": json_to_string_response,
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
