import requests
import json
import time
import random
import string

BASE_URL = "http://localhost:8000/v1/chat/completions"

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

def test_request(prompt, description):
    # Add random noise to prompt to bypass cache
    unique_prompt = f"{prompt} [Request ID: {generate_random_string()}]"
    
    print(f"\n--- Testing: {description} ---")
    print(f"Sending prompt: '{unique_prompt}'")
    
    payload = {
        "messages": [{"role": "user", "content": unique_prompt}],
        "model": "gpt-4o"
    }
    
    try:
        start = time.time()
        response = requests.post(BASE_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        duration = time.time() - start
        
        content = data['choices'][0]['message']['content']
        model_used = data.get('model', 'unknown')
        
        print(f"✅ Success in {duration:.2f}s")
        print(f"🤖 Response Model: {model_used}")
        print(f"📄 Content Snippet: {content[:100]}...")
        
        if "MOCK" in content:
            print("⚠️ WARNING: Still getting MOCK response!")
        else:
            print("🌟 REAL API RESPONSE CONFIRMED!")
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        # Try to print error body if available
        if hasattr(e, 'response') and e.response is not None:
             print(f"   Server says: {e.response.text}")

if __name__ == "__main__":
    print("🚀 Verifying REAL KEYS (Bypassing Cache)...")
    
    # 1. Simple -> Groq Real
    test_request("What is 2 + 2?", "Simple Query (Expect Groq)")
    
    # 2. Complex -> OpenAI/Gemini Real
    test_request("Write a python function to inverse a matrix using numpy", "Complex Query (Expect OpenAI or Gemini)")
