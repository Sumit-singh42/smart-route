import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv("backend/.env")

KEY = os.getenv("GROQ_API_KEY")
print(f"Testing Groq Key with different models...")

async def test_model(model_name):
    print(f"\n--- Testing Model: {model_name} ---")
    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": "hi"}],
        "model": model_name
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
            print(f"Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"Error Body: {resp.text}")
            else:
                print("SUCCESS!")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # Try the one we were using
    await test_model("llama3-8b-8192")
    # Try the new standard
    await test_model("llama-3.1-8b-instant")
    # Try a fallback
    await test_model("mixtral-8x7b-32768")

asyncio.run(main())
