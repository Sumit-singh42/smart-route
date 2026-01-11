import httpx
import json
import time
import asyncio
from app.core.config import settings
from app.core.cache import check_cache, save_to_cache

# Simple in-memory stats for MVP Phase 1 (Week 1)
STATS = {
    "total_requests": 0,
    "total_savings": 0.0,
    "cache_hits": 0,
    "cache_misses": 0,
    "provider_groq": 0,
    "provider_local": 0,
    "latest_request": {
        "type": "Waiting...",
        "provider": "Waiting...",
        "timestamp": 0
    }
}

# Cost per 1k input tokens (Approx)
COST_GPT4 = 0.03
COST_GROQ = 0.0005 
COST_GEMINI = 0.00035

class LLMProvider:
    async def route_request(self, messages: list):
        STATS["total_requests"] += 1
        
        # 1. CHECK CACHE
        cached_response = check_cache(messages)
        if cached_response:
            STATS["cache_hits"] += 1
            STATS["total_savings"] += COST_GPT4 
            cached_response["model"] = cached_response.get("model", "") + " (Cached)"
            return cached_response
            
        STATS["cache_misses"] += 1

        # 2. Analyze complexity
        is_complex = self._analyze_complexity(messages)

        # 3. Pick a provider
        response = None
        
        # LOGIC UPDATE: Since OpenAI key is flaky (429), we prefer Gemini for "Smart" queries if OpenAI fails
        # Or we can just default to Gemini for "Complex" if OpenAI is known bad.
        # For now, let's try OpenAI -> Fallback Gemini.
        
        if is_complex:
             # Check for Local LLM (Cost Savings!)
             if settings.LM_STUDIO_URL:
                 print(f"Routing to Local LLM (LM Studio) - Complex Query")
                 try:
                     response = await self._call_local_llm(messages)
                     STATS["total_savings"] += COST_GPT4 # We saved the full cost of GPT-4!
                     STATS["provider_local"] += 1
                     STATS["latest_request"] = {
                         "type": "Complex Query",
                         "provider": "LOCAL LLM",
                         "timestamp": time.time()
                     }
                     save_to_cache(messages, response)
                     return response
                 except Exception as e:
                     print(f"⚠️ Local LLM Failed: {e}. Falling back to Cloud Providers.")
             
             print(f"Routing to Smart Tier (Complex query)")
             # EMERGENCY FALLBACK: OpenAI/Gemini are 429/Expired. Using Groq Llama-3.1 for now.
             print(f"⚠️ Primary Smart Providers (OpenAI/Gemini) unavailable/quota-exceeded. Routing to Groq Llama-3.1 (High Performance).")
             # We use the same Groq method but maybe with a 'smart' prompt? For MVP just use Groq.
             try:
                 response = await self._call_groq(messages)
                 response["model"] = "llama-3.1 (Fallback for GPT-4)" # Annotate for dashboard
                 savings = COST_GPT4 - COST_GROQ
                 STATS["total_savings"] += savings
                 STATS["provider_groq"] += 1
                 STATS["latest_request"] = {
                     "type": "Complex Query (Fallback)",
                     "provider": "GROQ",
                     "timestamp": time.time()
                 }
                 save_to_cache(messages, response)
                 return response
             except Exception:
                 pass # If Groq fails, fall through...
                 
        elif not is_complex and settings.GROQ_API_KEY:
            print(f"Routing to Groq (Simple query)")
            response = await self._call_groq(messages)
            savings = COST_GPT4 - COST_GROQ
            STATS["total_savings"] += savings
            STATS["provider_groq"] += 1
            STATS["latest_request"] = {
                "type": "Simple Query",
                "provider": "GROQ",
                "timestamp": time.time()
            }
            save_to_cache(messages, response)
            return response
            
        else:
             raise Exception("No available providers configured")

    def _analyze_complexity(self, messages: list) -> bool:
        combined_text = " ".join([m.get("content", "") for m in messages])
        
        # Expanded keywords for "Smart" routing based on user feedback
        complex_keywords = [
            "code", "function", "python", "javascript", "react", "sql", # Coding
            "story", "poem", "essay", "novel", "haiku", # Creative Writing
            "logic", "reasoning", "solve", "math", "calculus", # Critical Thinking
            "analysis", "summary", "extract" # Data Processing
        ]
        
        if any(keyword in combined_text.lower() for keyword in complex_keywords):
            return True
        if len(combined_text) > 800:
            print("DEBUGGING COMPLEXITY: Length > 800 -> COMPLEX")
            return True
        print("DEBUGGING COMPLEXITY: Simple query")
        return False
        if len(combined_text) > 800:
            return True
        return False

    async def _call_local_llm(self, messages: list):
        if settings.USE_MOCK_LLM:
             # Reuse Groq mock for now as placeholder
             return await self._call_groq(messages)

        print(f"DEBUG: Calling Local LLM (Mythomax)...")
        headers = {"Content-Type": "application/json"}
        # LM Studio is OpenAI compatible!
        data = {
            "messages": messages,
            "model": "mythomax-l2-13b", # This is often ignored by LM Studio local server, but good practice
            "temperature": 0.7
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.LM_STUDIO_URL}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=120.0 # Local models can be slow
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"❌ Local LLM Error: {e.response.status_code} - {e.response.text}")
                raise e

    async def _call_groq(self, messages: list):
        if settings.USE_MOCK_LLM:
            await asyncio.sleep(0.5) # Simulate network latency
            return {
                "id": "mock-groq-123",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "llama-3.1-8b-instant",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": f"[MOCK GROQ] Simulated response for: {messages[-1]['content'][:20]}..."},
                    "finish_reason": "stop"
                }]
            }

        if not settings.GROQ_API_KEY:
            raise Exception("GROQ_API_KEY not set")
        
        print(f"DEBUG: Calling Groq (Llama-3.1)...")
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": messages,
            "model": "llama-3.1-8b-instant", # NEW MODEL ID
            "temperature": 0.7
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"❌ Groq Error: {e.response.status_code} - {e.response.text}")
                raise e

    async def _call_openai(self, messages: list):
        if settings.USE_MOCK_LLM:
            await asyncio.sleep(1.5) # Simulate standard latency
            return {
                "id": "mock-gpt4-123",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "gpt-4o",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": f"[MOCK GPT-4o] Intelligent simulated response for: {messages[-1]['content'][:20]}..."},
                    "finish_reason": "stop"
                }]
            }

        print(f"DEBUG: Calling OpenAI...")
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": messages,
            "model": "gpt-4o",
            "temperature": 0.7
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"❌ OpenAI Error: {e.response.status_code} - {e.response.text}")
                raise e

    async def _call_gemini(self, messages: list):
        if settings.USE_MOCK_LLM:
            await asyncio.sleep(1.0)
            return {
                "id": "mock-gemini-123",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "gemini-2.0-flash-001",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": f"[MOCK GEMINI] Balanced simulated response for: {messages[-1]['content'][:20]}..."},
                    "finish_reason": "stop"
                }]
            }

        print(f"DEBUG: Calling Gemini...")
        last_message = messages[-1]["content"]
        # Upgrading to Gemini 2.0 Flash as requested/available
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={settings.GEMINI_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": last_message}]}]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=data, timeout=30.0)
                response.raise_for_status()
                result = response.json()
                
                # Safe access to avoid index errors if safety filters block content
                try:
                    part = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0]
                    generated_text = part.get("text", "I'm sorry, I couldn't generate a response.")
                except IndexError:
                    print(f"⚠️ Gemini Safety Filter triggered or empty response: {result}")
                    generated_text = "I'm sorry, I couldn't generate a response (Safety Filter)."

                return {
                    "id": "chatcmpl-gemini",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": "gemini-2.0-flash-001",
                    "choices": [{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": generated_text
                        },
                        "finish_reason": "stop"
                    }]
                }
            except httpx.HTTPStatusError as e:
                print(f"❌ Gemini Error: {e.response.status_code} - {e.response.text}")
                raise e

provider_service = LLMProvider()
