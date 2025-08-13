from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.utils.auth import verify_token
from app.main import db

router = APIRouter()
applications = db.applications

class ApplicationCreate(BaseModel):
    job_title: str
    company: str
    description: Optional[str]
    status: str
    cover_letter_id: Optional[str]
    resume_id: Optional[str]

@router.post("/create")
async def create_application(data: ApplicationCreate, request: Request):
    try:
        user = await verify_token(request)

        user = request.state.user
        application_data = data.dict()
        application_data["user_id"] = user["uid"]
        result = applications.insert_one(application_data)
        return {"application_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-applications")
async def get_my_applications(request: Request):
    try:
        user = await verify_token(request)

        user = request.state.user
        apps = list(applications.find({"user_id": user["uid"]}))
        for app in apps:
            app["_id"] = str(app["_id"])
        return {"applications": apps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

