from fastapi import FastAPI, HTTPException
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.post("/summarize/")
async def summarize_resume(data: dict):
    resume_text = data.get("resume", "")

    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is required.")

    prompt = (
        f"You are a resume parser. Extract the following: "
        f"Name, Email, Skills, Experience, Education.\n"
        f"Resume: {resume_text}\nOutput in JSON format only."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return {"summary": response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
