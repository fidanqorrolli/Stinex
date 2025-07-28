from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from models.testimonial import Testimonial, TestimonialCreate, TestimonialUpdate
from typing import List
from datetime import datetime
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Setup logging
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/testimonials", tags=["testimonials"])

@router.get("/", response_model=List[Testimonial])
async def get_testimonials(approved_only: bool = True):
    """
    Get all testimonials.
    
    Parameters:
    - approved_only: If True, returns only approved testimonials (default: True for public view)
    """
    try:
        query = {"approved": True} if approved_only else {}
        testimonials = await db.testimonials.find(query).sort("created_at", -1).to_list(100)
        return [Testimonial(**testimonial) for testimonial in testimonials]
    except Exception as e:
        logger.error(f"Error fetching testimonials: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Laden der Kundenbewertungen."
        )

@router.get("/{testimonial_id}", response_model=Testimonial)
async def get_testimonial(testimonial_id: str):
    """
    Get a specific testimonial by ID.
    """
    try:
        testimonial = await db.testimonials.find_one({"id": testimonial_id})
        if not testimonial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bewertung nicht gefunden."
            )
        return Testimonial(**testimonial)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching testimonial {testimonial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Laden der Bewertung."
        )

@router.post("/", response_model=Testimonial, status_code=status.HTTP_201_CREATED)
async def create_testimonial(testimonial_data: TestimonialCreate):
    """
    Create a new testimonial (requires admin approval).
    """
    try:
        testimonial = Testimonial(**testimonial_data.dict())
        testimonial_dict = testimonial.dict()
        result = await db.testimonials.insert_one(testimonial_dict)
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fehler beim Speichern der Bewertung."
            )
        
        logger.info(f"New testimonial created: {testimonial.id}")
        return testimonial
        
    except Exception as e:
        logger.error(f"Error creating testimonial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Erstellen der Bewertung."
        )

@router.put("/{testimonial_id}/approve")
async def approve_testimonial(testimonial_id: str):
    """
    Approve a testimonial (admin only).
    """
    try:
        result = await db.testimonials.update_one(
            {"id": testimonial_id},
            {"$set": {"approved": True, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bewertung nicht gefunden."
            )
        
        logger.info(f"Testimonial approved: {testimonial_id}")
        return {"success": True, "message": "Bewertung erfolgreich genehmigt."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving testimonial {testimonial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Genehmigen der Bewertung."
        )

@router.put("/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(testimonial_id: str, testimonial_update: TestimonialUpdate):
    """
    Update a testimonial (admin only).
    """
    try:
        # Only update non-None fields
        update_data = {k: v for k, v in testimonial_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Keine Daten zum Aktualisieren bereitgestellt."
            )
        
        result = await db.testimonials.update_one(
            {"id": testimonial_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bewertung nicht gefunden."
            )
        
        # Return updated testimonial
        updated_testimonial = await db.testimonials.find_one({"id": testimonial_id})
        return Testimonial(**updated_testimonial)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating testimonial {testimonial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Aktualisieren der Bewertung."
        )

@router.delete("/{testimonial_id}")
async def delete_testimonial(testimonial_id: str):
    """
    Delete a testimonial (admin only).
    """
    try:
        result = await db.testimonials.delete_one({"id": testimonial_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bewertung nicht gefunden."
            )
        
        logger.info(f"Testimonial deleted: {testimonial_id}")
        return {"success": True, "message": "Bewertung erfolgreich gelöscht."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting testimonial {testimonial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Löschen der Bewertung."
        )