from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

class ServiceCategory(str, Enum):
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    INDUSTRIAL = "industrial"

class ServiceCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    pricing: str = Field(..., max_length=50)
    features: List[str] = Field(..., min_items=1)
    category: ServiceCategory
    active: bool = True

class Service(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    pricing: str
    features: List[str]
    category: ServiceCategory
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Büroreinigung",
                "description": "Professionelle Reinigung für Büros, Praxen und Verwaltungsgebäude",
                "pricing": "Ab 15€ pro Stunde",
                "features": [
                    "Tägliche oder wöchentliche Reinigung",
                    "Schreibtische und Arbeitsflächen",
                    "Sanitäranlagen und Küchen"
                ],
                "category": "commercial",
                "active": True,
                "created_at": "2025-01-28T10:30:00Z",
                "updated_at": "2025-01-28T10:30:00Z"
            }
        }

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    pricing: Optional[str] = None
    features: Optional[List[str]] = None
    category: Optional[ServiceCategory] = None
    active: Optional[bool] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)