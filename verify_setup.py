import requests
import json
import time

BASE_URL = "http://localhost:8000/v1/chat/completions"

def test_request(prompt, description):
    print(f"\n--- Testing: {description} ---")
    print(f"Sending prompt: '{prompt[:50]}...'")
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4o" # We ask for GPT-4, but the proxy might give us something else!
    }
    
    try:
        start = time.time()
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        duration = time.time() - start
        
        # Extract meaningful info
        content = data['choices'][0]['message']['content']
        # Some providers return 'model' in the response, let's see what they say
        model_used = data.get('model', 'unknown')
        
        print(f"✅ Success in {duration:.2f}s")
        print(f"🤖 Response Model: {model_used}")
        print(f"📄 Content Snippet: {content[:100]}...")
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Server Traceback: {e.response.text}")

if __name__ == "__main__":
    print("🚀 Verifying SmartRoute Proxy...")
    
    # 1. Simple Request -> Expect Groq (Llama-3)
    test_request("What is the capital of Spain?", "Simple Query (Should Route to Cheap/Fast Model)")
    
    # 2. Complex Request -> Expect OpenAI (GPT-4)
    # We force 'complex' by adding the word 'code' or 'function' as per our heuristic in providers.py
    test_request("Write a python function to sort a list using merge sort", "Complex Query (Should Route to Smart Model)")
    
    print("\n✨ Done! Check your Dashboard at http://localhost:5173 to see the stats update!")
