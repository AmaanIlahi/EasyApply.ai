from fastapi import APIRouter, Request, UploadFile, File, Depends, Form, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.documentSchema import DocumentResponse
from app.utils.auth import verify_token
from app.utils.gemini import clean_text_with_gemini
# from app.database import get_mongo_db
from datetime import datetime
import logging
from app.db import db

router = APIRouter()
security = HTTPBearer()

@router.post("/submit-document", response_model=DocumentResponse)
async def submit_document(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(security),
    file: UploadFile = File(None),
    manual_input: str = Form(None),
):
    try:
        await verify_token(request)
        user_id = request.state.user
        print("User Id : ", user_id)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_text = None
        source_type = None

        if file:
            source_type = "upload"
            try:
                contents = await file.read()
                new_text = contents.decode("utf-8", errors="ignore")
            except Exception as e:
                logging.error(f"File read error: {e}")
                raise HTTPException(status_code=500, detail="Error reading file")
        elif manual_input:
            source_type = "manual"
            new_text = manual_input.strip()
        else:
            raise HTTPException(status_code=400, detail="No content provided")

        if not new_text:
            raise HTTPException(status_code=400, detail="No valid text extracted")

        collection = db["user-info"]
        existing_doc = await collection.find_one({"user_id": user_id})

        if existing_doc:
            # Append new text to existing raw_text
            updated_raw = existing_doc["raw_text"] + "\n" + new_text
        else:
            updated_raw = new_text

        try:
            updated_cleaned = await clean_text_with_gemini(updated_raw)
        except Exception as e:
            logging.error(f"Gemini API error: {e}")
            raise HTTPException(status_code=500, detail="Gemini processing failed")

        new_data = {
            "raw_text": updated_raw,
            "cleaned_text": updated_cleaned,
            "source_type": source_type,
            "timestamp": datetime.utcnow()
        }

        print(new_data)

        if existing_doc:
            await collection.update_one(
                {"user_id": user_id},
                {"$set": new_data}
            )
        else:
            new_data["user_id"] = user_id
            await collection.insert_one(new_data)

        return DocumentResponse(user_id=user_id, **new_data)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Unhandled server error: {e}")
        raise HTTPException(status_code=500, detail="Unhandled server error")
