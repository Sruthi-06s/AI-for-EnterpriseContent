import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

print(f"API Key found: {API_KEY is not None}")

if API_KEY:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # These are the CURRENT Groq models as of 2026
    current_models = [
        "deepseek-r1-distill-llama-70b",
        "llama-3.3-70b-versatile",
        "llama-3.3-70b-specdec",
        "qwen-qwq-32b",
        "qwen-2.5-32b"
    ]

    print("\n🔍 Testing current Groq models...\n")

    for model in current_models:
        print(f"Testing: {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'API works!' in one short sentence"}],
            "max_tokens": 30
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ WORKING! Response: {result['choices'][0]['message']['content']}\n")
                print(f"🎯 Use this model: {model}")
                break
            else:
                print(f"❌ Status {response.status_code}: {response.text[:120]}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
else:
    print("❌ No API key found")