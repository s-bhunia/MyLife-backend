# schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class IntentRequest(BaseModel):
    text: str

class FeedbackRequest(BaseModel):
    name: str = "Anonymous"
    email: Optional[EmailStr] = None
    message: str
    
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, v):
        if v == '' or v is None:
            return None
        return v