from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class ContactStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the contact")
    email: EmailStr = Field(..., description="Valid email address")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number (optional)")
    service: Optional[str] = Field(None, max_length=50, description="Requested service type")
    message: str = Field(..., min_length=1, max_length=2000, description="Contact message")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Max Mustermann",
                "email": "max@beispiel.de",
                "phone": "+49 123 456 789",
                "service": "Büroreinigung",
                "message": "Ich interessiere mich für eine regelmäßige Büroreinigung für unser 200qm Büro."
            }
        }

class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    service: Optional[str] = None
    message: str
    status: ContactStatus = ContactStatus.NEW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Max Mustermann",
                "email": "max@beispiel.de",
                "phone": "+49 123 456 789",
                "service": "Büroreinigung",
                "message": "Ich interessiere mich für eine regelmäßige Büroreinigung.",
                "status": "new",
                "created_at": "2025-01-28T10:30:00Z",
                "updated_at": "2025-01-28T10:30:00Z"
            }
        }

class ContactResponse(BaseModel):
    success: bool = True
    message: str
    submission_id: str
    estimated_response: str = "24 Stunden"

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns binnen 24 Stunden bei Ihnen.",
                "submission_id": "123e4567-e89b-12d3-a456-426614174000",
                "estimated_response": "24 Stunden"
            }
        }

class ContactUpdate(BaseModel):
    status: Optional[ContactStatus] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "validation_error",
                "message": "Bitte füllen Sie alle Pflichtfelder aus."
            }
        }