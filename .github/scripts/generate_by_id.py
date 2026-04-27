import os
import requests
from github import Github

# Get the info from GitHub's environment
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
TICKET_ID = os.getenv('TICKET_ID')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def get_ai_response(title, body):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    prompt = f"Act as a QA Engineer. Write test cases for this ticket:\nTitle: {title}\nDescription: {body}"
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

# Initialize GitHub connection
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
issue = repo.get_issue(number=int(TICKET_ID))

# Generate and post
test_cases = get_ai_response(issue.title, issue.body)
issue.create_comment(f"### 🤖 Automated Test Cases\n\n{test_cases}")
