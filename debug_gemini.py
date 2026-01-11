import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv("backend/.env")

KEY = os.getenv("GEMINI_API_KEY")
print(f"Testing Gemini Key: {KEY[:10]}...")

async def test():
    # Use the REST API URL we used in providers.py
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={KEY}"
    data = {
        "contents": [{"parts": [{"text": "Hello"}]}]
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=data)
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
