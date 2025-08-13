from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    manual_input: Optional[str] = None

class DocumentResponse(BaseModel):
    user_id: str
    raw_text: str
    cleaned_text: str
    source_type: str
    timestamp: datetime
