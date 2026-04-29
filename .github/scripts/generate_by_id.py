import os
import requests
from github import Github

# 1. Get Environment Variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ISSUE_NUMBER = int(os.getenv('ISSUE_NUMBER'))
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def get_ai_test_cases(issue_title, issue_body):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    prompt = f"""
    Act as a Senior QA Automation Engineer. Based on the following GitHub Issue, write a set of 
    manual test cases including:
    - Positive Cases
    - Negative Cases
    - Edge Cases
    Format the output in clear Markdown with 'Steps to Reproduce' and 'Expected Result'.

    TICKET TITLE: {issue_title}
    TICKET DESCRIPTION: {issue_body}
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']

# 2. Connect to GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
issue = repo.get_issue(number=ISSUE_NUMBER)

# 3. Generate and Post the comment
try:
    test_cases = get_ai_test_cases(issue.title, issue.body)
    issue.create_comment(f"### 🤖 AI-Generated Test Cases\n\n{test_cases}")
except Exception as e:
    issue.create_comment(f"❌ Error generating test cases: {str(e)}")
