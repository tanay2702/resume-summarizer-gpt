from fastapi import FastAPI
import requests, os

app = FastAPI()
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.post("/summarize/")
async def summarize_resume(data: dict):
    resume_text = data.get("resume", "")
    payload = {"inputs": resume_text}
    response = requests.post(
        "https://api-inference.huggingface.co/models/openai/whisper-base",  # choose a free model
        headers=HEADERS,
        json=payload
    )
    return response.json()
