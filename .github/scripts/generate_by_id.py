def get_ai_test_cases(issue_title, issue_body):
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY is missing in GitHub Secrets."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    # Updated Prompt for High-Level Format
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
        "temperature": 0.2 # Lower temperature makes the output more focused and less "wordy"
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
