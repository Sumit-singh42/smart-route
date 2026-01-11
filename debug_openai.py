import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv("backend/.env")

KEY = os.getenv("OPENAI_API_KEY")
print(f"Testing OpenAI Key: {KEY[:10]}...")

async def test():
    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": "hi"}],
        "model": "gpt-3.5-turbo" # Use cheap model for ping
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
