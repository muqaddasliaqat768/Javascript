import os
import requests
from github import Github, Auth

# 1. Fetch variables from GitHub Actions
api_key = os.getenv('GROQ_API_KEY', '').strip()
token = os.getenv('GITHUB_TOKEN')
ticket_number = os.getenv('TICKET_ID')  # This captures what you type in the 'Run workflow' box
repo_name = os.getenv('GITHUB_REPOSITORY')

def get_test_cases(title, body):
    if not body or len(body) < 10:
        return "⚠️ Error: Ticket description is too short for AI to analyze."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    # Strictly single-line format as requested
    prompt = f"""
    Act as a Senior QA Engineer. Provide ONLY single-line test scenarios. 
    Format: * Check "[Scenario Name]"
    Categories: ### Positive Cases, ### Negative Cases, ### Edge Cases.
    Ticket: {title} - {body}
    """
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# 2. Connect to GitHub and post to the SPECIFIC ticket number
try:
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    
    # We convert ticket_number to an integer to find the right one
    issue = repo.get_issue(number=int(ticket_number))
    
    results = get_test_cases(issue.title, issue.body)
    issue.create_comment(f"### 🤖 Automated Test Cases\n\n{results}")
    print(f"Successfully posted to Ticket #{ticket_number}")
except Exception as e:
    print(f"Failed to post: {str(e)}")
