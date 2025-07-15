# Sample prompt engineering logic (expand as needed)
def get_resume_prompt(resume_text: str) -> str:
    return f"""
    You are a resume parser.
    Extract the following: Name, Email, Skills, Experience, Education.
    Resume: {resume_text}
    Output in JSON format.
    """