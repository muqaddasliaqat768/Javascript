import os
import requests
import sys
from github import Github

# 1. Get Environment Variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# Changed this to match the YAML variable name
ISSUE_ID_STR = os.getenv('ISSUE_ID') 

def get_ai_test_cases(issue_title, issue_body):
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY is missing in GitHub Secrets."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    prompt = f"""
    Act as a Senior QA Automation Engineer. Write manual test cases (Positive, Negative, Edge Cases) 
    in Markdown for:
    TITLE: {issue_title}
    DESCRIPTION: {issue_body}
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if 'choices' in data:
            return data['choices'][0]['message']['content']
        else:
            return f"❌ API Error: Unexpected response format: {data}"
            
    except Exception as e:
        return f"❌ Failed to reach Groq API: {str(e)}"

# 2. Main Logic
if __name__ == "__main__":
    try:
        # Check if ISSUE_ID_STR is actually present
        if not ISSUE_ID_STR:
            print("❌ Error: ISSUE_ID is missing from environment variables.")
            sys.exit(1)

        print(f"Connecting to repo: {REPO_NAME}...")
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        
        print(f"Fetching Ticket #{ISSUE_ID_STR}...")
        issue = repo.get_issue(number=int(ISSUE_ID_STR))

        print("Generating test cases via Groq AI...")
        test_cases = get_ai_test_cases(issue.title, issue.body)
        
        print("Posting comment to GitHub...")
        issue.create_comment(f"### 🤖 AI-Generated Test Cases\n\n{test_cases}")
        print("✓ Done! Test cases posted successfully.")
        
    except Exception as e:
        print(f"❌ Workflow failed: {str(e)}")
        sys.exit(1)
