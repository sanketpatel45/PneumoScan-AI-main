import requests
import json

HUGGINGFACE_API_URL = "https://router.huggingface.co/together/v1/chat/completions"
HUGGINGFACE_API_KEY = "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"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [
        {
            "role": "system",
            "content": "You are PneumoScan AI, a medical assistant specialized in pneumonia detection."
        },
        {
            "role": "user",
            "content": "What are the symptoms of pneumonia?"
        }
    ],
    "parameters": {
        "temperature": 0.7,
        "max_new_tokens": 300,
        "return_full_text": False,
        "repetition_penalty": 1.2
    },
    "model": "deepseek-ai/DeepSeek-R1"  # Replace with a valid model if needed
}

response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
print(response.status_code)
print(response.json())
