def get_test_cases(title, body):
    if not api_key:
        return "❌ Error: GROQ_API_KEY is not found in Secrets."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    # This prompt strictly forbids headers and labels
    prompt = f"""
    Act as a Senior QA Engineer. Analyze the ticket below and provide a simple list of test scenarios.
    
    STRICT RULES:
    1. Output ONLY the test scenarios.
    2. Start every line with a bullet point and the word "Check". 
       Example: * Check "Description of the test"
    3. DO NOT include headers like "Positive Cases", "Negative Cases", or "Edge Cases".
    4. DO NOT include any introductory or concluding text.
    5. Provide ONLY the list.

    Ticket Title: {title}
    Ticket Description: {body}
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
