import os
import requests
from github import Github

# 1. Get and CLEAN the API Key
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '').strip() # .strip() removes accidental spaces
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
TICKET_ID = os.getenv('TICKET_ID')
REPO_NAME = os.getenv('GITHUB_REPOSITORY')

def get_ai_response(title, body):
    # Safety Check: If key is missing, stop here
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY is missing in GitHub Secrets."

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    # Updated Header Format
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Act as a Senior QA Engineer. Analyze the ticket below and generate test cases.
    FOR EACH CASE (Positive, Negative, and Edge Cases), provide ONLY:
    1. Test Case ID (Format: TC-00X - [Short Title])
    2. Test Case Description (A brief summary of the objective)
    
    TICKET TITLE: {title}
    TICKET DESCRIPTION: {body}
    """
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() # This will catch errors like 401 Unauthorized
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ AI API Error: {str(e)}"

# Rest of your script (GitHub connection part) stays the same
