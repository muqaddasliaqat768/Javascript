def get_test_cases(title, body):
    if not api_key:
        return "❌ Error: GROQ_API_KEY is not found in Secrets."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # This prompt tells the AI exactly what to EXCLUDE
    prompt = f"""
    Act as a Senior QA Engineer. Analyze the ticket below and generate a list of test cases.
    
    STRICT RULES:
    1. For every test case, provide ONLY:
       - Test Case ID: TC-00X - [Title]
       - Test Case Description: [One sentence summary]
    2. DO NOT include "Steps", "Expected Results", "Preconditions", or "Environment".
    3. DO NOT include any introductory text or conclusions.
    4. Group them by: ### Positive, ### Negative, and ### Edge Cases.

    Ticket Title: {title}
    Ticket Description: {body}
    """
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1 # Keep it low so the AI doesn't get creative
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ AI Error: {str(e)}"
