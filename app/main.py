from fastapi import FastAPI, Request
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/summarize/")
async def summarize_resume(data: dict):
    resume_text = data.get("resume", "")
    prompt = f"You are a resume parser. Extract the following: Name, Email, Skills, Experience, Education.\nResume: {resume_text}\nOutput in JSON format."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return {"summary": response.choices[0].message['content']}