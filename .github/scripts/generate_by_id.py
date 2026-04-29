import os
import requests
from github import Github

# 1. Get Environment Variables with safety fallbacks
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
ISSUE_ID = os.getenv('ISSUE_NUMBER')

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
        response.raise_for_status() # Check for 401, 404, 500 errors
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
        # Ensure we have an issue number
        if not ISSUE_ID:
            print("No ISSUE_NUMBER found. Skipping.")
            exit(0) # Exit gracefully

        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        issue = repo.get_issue(number=int(ISSUE_ID))

        test_cases = get_ai_test_cases(issue.title, issue.body)
        issue.create_comment(f"### 🤖 AI-Generated Test Cases\n\n{test_cases}")
        
    except Exception as e:
        print(f"Workflow failed: {e}")
        exit(1) # Only exit 1 if it's a critical system failure
