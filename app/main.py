from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

class ResumeRequest(BaseModel):
    resume: str

app = FastAPI()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise Exception("HF_TOKEN is not set")

MODEL = "facebook/bart-large-cnn"
HF_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

@app.post("/summarize/")
async def summarize_resume(req: ResumeRequest):
    text = req.resume
    text = " ".join(text.splitlines())

    resp = requests.post(
        HF_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=f"HF API error {resp.status_code}: {resp.text}")
    
    return resp.json()
