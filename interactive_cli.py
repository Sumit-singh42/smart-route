import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000/v1/chat/completions"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def type_writer(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)
    print("")

def send_query(prompt):
    print(f"\n{BLUE}🚀 Routing...{RESET}")
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4o" # The proxy decides the REAL model
    }
    
    try:
        start = time.time()
        response = requests.post(BASE_URL, json=payload)
        duration = time.time() - start
        
        if response.status_code != 200:
            print(f"{RED}❌ Error {response.status_code}: {response.text}{RESET}")
            return

        data = response.json()
        content = data['choices'][0]['message']['content']
        model_used = data.get('model', 'unknown')
        
        # Color code the model to show intelligence
        model_color = YELLOW if "llama" in model_used else GREEN
        if "Cached" in model_used:
            model_color = BLUE

        print(f"✅ Resolved in {duration:.2f}s")
        print(f"🤖 Model: {model_color}{model_used}{RESET}")
        print(f"📄 Response:")
        print(f"{'-'*40}")
        type_writer(content)
        print(f"{'-'*40}")

    except Exception as e:
        print(f"{RED}❌ Connection Failed: {e}{RESET}")

def main():
    print(f"{GREEN}====================================={RESET}")
    print(f"{GREEN}    SmartRoute Interactive CLI       {RESET}")
    print(f"{GREEN}====================================={RESET}")
    print("Type your prompt and press Enter.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input(f"{YELLOW}You > {RESET}")
            if user_input.lower() in ['exit', 'quit']:
                print("Bye! 👋")
                break
            
            if not user_input.strip():
                continue

            send_query(user_input)
            
        except KeyboardInterrupt:
            print("\nBye! 👋")
            break

if __name__ == "__main__":
    main()
