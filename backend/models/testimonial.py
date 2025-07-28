from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TestimonialCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    company: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=1000)
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")
    approved: bool = False

class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company: str
    text: str
    rating: int = Field(..., ge=1, le=5)
    approved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Maria Schmidt",
                "company": "Schmidt & Partner",
                "text": "Stinex reinigt unsere Büroräume seit 2 Jahren. Immer zuverlässig und gründlich!",
                "rating": 5,
                "approved": True,
                "created_at": "2025-01-28T10:30:00Z",
                "updated_at": "2025-01-28T10:30:00Z"
            }
        }

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    text: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    approved: Optional[bool] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)