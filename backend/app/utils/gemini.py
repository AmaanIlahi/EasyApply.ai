import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model = genai.GenerativeModel("gemini-pro")
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


async def clean_text_with_gemini(text):
    # models = genai.list_models()
    # for model in models:
    #     print(model.name,
    #           "supports generate_content" if "generateContent" in model.supported_generation_methods else "NO generate_content")

    # print(text)
    prompt = (
        "Clean and summarize this text by removing boilerplate, headers, footers, and unrelated information:\n\n"
        f"{text}"
    )
    response = model.generate_content(prompt)
    # print(response.text.strip())
    return response.text.strip()



async def generate_cover_letter(user_summary: str, job_description: str) -> str:
    prompt = f"""
Using the candidate's resume summary below, write a personalized and professional cover letter for the given job description. 
Tailor the content to highlight relevant experience, skills, and enthusiasm for the role.

Candidate Resume Summary:
{user_summary}

Job Description:
{job_description}

Cover Letter:
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] Failed to generate cover letter: {e}")
        return "Error generating cover letter. Please try again later."

