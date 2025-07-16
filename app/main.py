from fastapi import FastAPI, HTTPException
import os
import requests

app = FastAPI()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise Exception("HF_TOKEN not found in environment variables")

MODEL = "facebook/bart-large-cnn"
HF_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

@app.post("/summarize/")
async def summarize_resume(data: dict):
    text = data.get("resume", "")
    if not text:
        raise HTTPException(status_code=400, detail="Missing resume text")
    
    resp = requests.post(HF_URL, headers={"Authorization": f"Bearer {HF_TOKEN}"}, json={"inputs": text})
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=f"HF API error {resp.status_code}: {resp.text}")
    
    return resp.json()
