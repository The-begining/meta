import os
import requests

# ✅ Fetch API key from environment
NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY")
NEBIUS_API_URL = "https://api.studio.nebius.ai/v1/chat/completions"  # Corrected URL

def test_nebius_api():
    headers = {
        "Authorization": f"Bearer {NEBIUS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "max_tokens": 705,
        "temperature": 0.37,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ]
    }

    try:
        response = requests.post(NEBIUS_API_URL, headers=headers, json=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print(f"API Request Error: {e}")

# 🚀 Run the test
test_nebius_api()
