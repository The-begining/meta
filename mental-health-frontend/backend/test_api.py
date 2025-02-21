import os
import requests

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
NEBIUS_API_URL = "https://api.studio.nebius.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {NEBIUS_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "meta-llama/Llama-3.3-70B-Instruct",
    "max_tokens": 50,
    "temperature": 0.7,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
}

try:
    response = requests.post(NEBIUS_API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("API Request Error:", e)
