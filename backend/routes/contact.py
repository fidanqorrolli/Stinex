from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from models.contact import Contact, ContactCreate, ContactResponse, ErrorResponse
from typing import List
import os
import logging

# Setup logging
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact_data: ContactCreate):
    """
    Create a new contact submission.
    
    This endpoint handles contact form submissions from the website.
    All submitted contacts are stored in the database with a 'new' status.
    """
    try:
        # Create contact object
        contact = Contact(**contact_data.dict())
        
        # Insert into database
        contact_dict = contact.dict()
        result = await db.contacts.insert_one(contact_dict)
        
        if not result.inserted_id:
            logger.error("Failed to insert contact into database")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fehler beim Speichern der Nachricht. Bitte versuchen Sie es erneut."
            )
        
        logger.info(f"New contact submission created: {contact.id}")
        
        # Return success response
        return ContactResponse(
            success=True,
            message="Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns binnen 24 Stunden bei Ihnen.",
            submission_id=contact.id,
            estimated_response="24 Stunden"
        )
        
    except Exception as e:
        logger.error(f"Error creating contact: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ein unerwarteter Fehler ist aufgetreten. Bitte versuchen Sie es später erneut."
        )

@router.get("/", response_model=List[Contact])
async def get_contacts(skip: int = 0, limit: int = 100):
    """
    Get all contact submissions (for admin use).
    
    Parameters:
    - skip: Number of records to skip (for pagination)
    - limit: Number of records to return (max 100)
    """
    try:
        contacts = await db.contacts.find().skip(skip).limit(limit).sort("created_at", -1).to_list(limit)
        return [Contact(**contact) for contact in contacts]
    except Exception as e:
        logger.error(f"Error fetching contacts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Laden der Kontakte."
        )

@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: str):
    """
    Get a specific contact submission by ID.
    """
    try:
        contact = await db.contacts.find_one({"id": contact_id})
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kontakt nicht gefunden."
            )
        return Contact(**contact)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching contact {contact_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Laden des Kontakts."
        )

@router.put("/{contact_id}/status")
async def update_contact_status(contact_id: str, status_update: dict):
    """
    Update the status of a contact submission.
    """
    try:
        valid_statuses = ["new", "in_progress", "completed"]
        new_status = status_update.get("status")
        
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ungültiger Status. Erlaubte Werte: {valid_statuses}"
            )
        
        result = await db.contacts.update_one(
            {"id": contact_id},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kontakt nicht gefunden."
            )
        
        return {"success": True, "message": "Status erfolgreich aktualisiert."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating contact status {contact_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Aktualisieren des Status."
        )