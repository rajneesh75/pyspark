from typing import TypedDict, List
from langchain_core.messages import BaseMessage
import os
import requests


class AgentState(TypedDict):
    messages: List[BaseMessage]
    category: str  # We will store the classification here (Math vs General)


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = False

headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json",
           "Content-Type": "application/json", }

prompt = "Explain the theory of relativity in simple terms."

payload = {
    "model": "meta/llama-4-maverick-17b-128e-instruct",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 1024,
    "temperature": 1.00,
    "top_p": 1.00,
    "frequency_penalty": 0.00,
    "presence_penalty": 0.00,
    "stream": stream
}

response = requests.post(NVIDIA_URL, headers=headers, json=payload)
print(response)
json_resp = response.json()
print(json_resp)

 
