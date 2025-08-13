import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(resume_text, job_desc, tone="Formal"):
    prompt = f"""Generate a {tone.lower()} cover letter based on the following resume and job description.\nResume: {resume_text}\nJob Description: {job_desc}"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

