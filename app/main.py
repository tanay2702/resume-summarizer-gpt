from fastapi import FastAPI, HTTPException, Request, File, UploadFile
import os, requests

app = FastAPI()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise Exception("HF_TOKEN not set in environment")

MODEL = "facebook/bart-large-cnn"
HF_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

@app.post("/summarize/raw")
async def summarize_raw(request: Request):
    raw = await request.body()
    text = raw.decode(errors="ignore")
    if not text.strip():
        raise HTTPException(400, "Empty resume text")
    resp = requests.post(HF_URL,
                         headers={"Authorization": f"Bearer {HF_TOKEN}"},
                         json={"inputs": text})
    if resp.status_code != 200:
        raise HTTPException(500, f"HF error {resp.status_code}")
    return resp.json()

@app.post("/summarize/file")
async def summarize_file(file: UploadFile = File(...)):
    content = (await file.read()).decode(errors="ignore")
    if not content.strip():
        raise HTTPException(400, "Empty file")
    resp = requests.post(HF_URL,
                         headers={"Authorization": f"Bearer {HF_TOKEN}"},
                         json={"inputs": content})
    if resp.status_code != 200:
        raise HTTPException(500, f"HF error {resp.status_code}")
    return resp.json()
