from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.utils.auth import verify_token
from app.utils.gemini import generate_cover_letter
from app.db import db
import logging

router = APIRouter()
security = HTTPBearer()

class JDInput(BaseModel):
    job_description: str

@router.post("/generate-cover-letter")
async def generate_cover_letter_endpoint(
    request: Request,
    jd_input: JDInput,
    token: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        await verify_token(request)
        user_id = request.state.user
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch cleaned resume text from DB
        collection = db["user-info"]
        user_doc = await collection.find_one({"user_id": user_id})
        if not user_doc or "cleaned_text" not in user_doc:
            raise HTTPException(status_code=404, detail="User resume summary not found")

        user_summary = user_doc["cleaned_text"]
        job_description = jd_input.job_description

        cover_letter = await generate_cover_letter(user_summary, job_description)

        return { "cover_letter": cover_letter }

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Cover letter generation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
