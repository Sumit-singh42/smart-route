
import httpx
import asyncio

async def send_complex_request():
    url = "http://localhost:8000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [{"role": "user", "content": "Write python code"}]
    }
    print(f"Sending request to {url}...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=30.0)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    asyncio.run(send_complex_request())
