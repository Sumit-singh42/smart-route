
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")

async def test_local_llm():
    print(f"Testing Chat Completion to: {LM_STUDIO_URL}/chat/completions")
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [{"role": "user", "content": "Hello"}],
        "model": "local-model",
        "temperature": 0.7
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LM_STUDIO_URL}/chat/completions",
                headers=headers,
                json=data,
                timeout=10.0
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Chat Completion Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_local_llm())
