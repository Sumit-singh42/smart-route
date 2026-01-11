import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv("backend/.env")

KEY = os.getenv("GEMINI_API_KEY")

async def list_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={KEY}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                models = resp.json().get('models', [])
                print("Available Models:")
                for m in models:
                    if 'generateContent' in m.get('supportedGenerationMethods', []):
                        print(f" - {m['name']}")
            else:
                print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(list_models())
