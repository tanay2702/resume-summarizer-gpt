from fastapi import FastAPI, HTTPException
import os
import requests

app = FastAPI()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise Exception("HF_TOKEN not provided in environment variables")

HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

@app.post("/summarize/")
async def summarize_resume(data: dict):
    resume_text = data.get("resume", "")
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is required")

    payload = {"inputs": resume_text}
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    resp = requests.post(HF_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=f"HF API error {resp.status_code}: {resp.text}")
    return resp.json()
