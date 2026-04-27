def get_test_cases(title, body):
    if not api_key:
        return "❌ Error: GROQ_API_KEY is not found in Secrets."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # This prompt is strictly optimized for single-line scenarios
    prompt = f"""
    Act as a Senior QA Engineer. Analyze the ticket below and provide ONLY a single-line title for each test case.
    
    STRICT FORMATTING RULES:
    1. Output ONLY the test case title (e.g., Check "Login with valid email").
    2. DO NOT include "Test Case ID" or "TC-001".
    3. DO NOT include "Description", "Steps", or "Expected Results".
    4. Group them ONLY by these headers: ### Positive Cases, ### Negative Cases, ### Edge Cases.
    5. Each test case must be a single line bullet point.

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
