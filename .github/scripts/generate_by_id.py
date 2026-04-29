import os
import requests
import sys
from github import Github

# 1. Get Environment Variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# This MUST match the name in the YAML env section
ISSUE_ID_STR = os.getenv('ISSUE_ID') 

def get_ai_test_cases(issue_title, issue_body):
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY is missing."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""
    Act as a Senior QA Automation Engineer. Based on the GitHub Issue below, 
    generate a concise list of high-level Use Cases. 

    STRICT FORMATTING RULES:
    1. Start with the header "UseCases:"
    2. Use the format: Check "[Brief description of the scenario]"
    3. DO NOT include 'Steps to Reproduce', 'Expected Results', or 'Positive/Negative' labels.
    4. Keep it to one line per use case.
    5. Include a final line for "Cross-Browser Testing".

    TICKET TITLE: {issue_title}
    TICKET DESCRIPTION: {issue_body}
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Failed to reach Groq API: {str(e)}"

if __name__ == "__main__":
    try:
        # Check if ID was passed correctly
        if not ISSUE_ID_STR:
            print("❌ ERROR: ISSUE_ID is missing from Environment Variables.")
            sys.exit(1)

        print(f"Connecting to Repo: {REPO_NAME}")
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        
        print(f"Fetching Ticket #{ISSUE_ID_STR}...")
        issue = repo.get_issue(number=int(ISSUE_ID_STR))

        print("Generating Use Cases...")
        test_cases = get_ai_test_cases(issue.title, issue.body)
        
        print(f"AI Content Generated. Length: {len(test_cases)}")
        
        # Post the comment
        issue.create_comment(f"### 🤖 AI-Generated Use Cases\n\n{test_cases}")
        print("✓ SUCCESS: Comment added to the ticket.")

    except Exception as e:
        print(f"❌ CRITICAL WORKFLOW ERROR: {str(e)}")
        sys.exit(1)
