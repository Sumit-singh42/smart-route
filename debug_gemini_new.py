import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv("backend/.env")

KEY = os.getenv("GEMINI_API_KEY")
print(f"Testing Gemini Key: {KEY[:10]}...")

async def test():
    # Trying gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={KEY}"
    data = {
        "contents": [{"parts": [{"text": "Hello, are you working?"}]}]
    }
    try:
        async with httpx.AsyncClient() as client:
            print(f"POSTing to {url.split('?')[0]}...")
            resp = await client.post(url, json=data)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
