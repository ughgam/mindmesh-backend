from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
# Shared properties
class ArticleBase(BaseModel):
    url: HttpUrl
    title: Optional[str] = None
    categories: Optional[str] = None

# Properties to receive on article creation
class ArticleCreate(ArticleBase):
    extracted_text: Optional[str] = None
    metadata_info: Optional[Dict[str, Any]] = None

# Properties to return to the frontend
class ArticleResponse(ArticleBase):
    id: int
    user_id: int
    created_at: datetime
    extracted_text: Optional[str] = None
    metadata_info: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
