from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from models.service import Service, ServiceCreate, ServiceUpdate
from typing import List
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

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=List[Service])
async def get_services(active_only: bool = True):
    """
    Get all services.
    
    Parameters:
    - active_only: If True, returns only active services (default: True)
    """
    try:
        query = {"active": True} if active_only else {}
        services = await db.services.find(query).sort("created_at", 1).to_list(100)
        return [Service(**service) for service in services]
    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Laden der Services."
        )

@router.get("/{service_id}", response_model=Service)
async def get_service(service_id: str):
    """
    Get a specific service by ID.
    """
    try:
        service = await db.services.find_one({"id": service_id})
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service nicht gefunden."
            )
        return Service(**service)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching service {service_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Laden des Services."
        )

@router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED)
async def create_service(service_data: ServiceCreate):
    """
    Create a new service (admin only).
    """
    try:
        service = Service(**service_data.dict())
        service_dict = service.dict()
        result = await db.services.insert_one(service_dict)
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fehler beim Erstellen des Services."
            )
        
        logger.info(f"New service created: {service.id}")
        return service
        
    except Exception as e:
        logger.error(f"Error creating service: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Erstellen des Services."
        )

@router.put("/{service_id}", response_model=Service)
async def update_service(service_id: str, service_update: ServiceUpdate):
    """
    Update a service (admin only).
    """
    try:
        # Only update non-None fields
        update_data = {k: v for k, v in service_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Keine Daten zum Aktualisieren bereitgestellt."
            )
        
        result = await db.services.update_one(
            {"id": service_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service nicht gefunden."
            )
        
        # Return updated service
        updated_service = await db.services.find_one({"id": service_id})
        return Service(**updated_service)
        
    except HTTPException:
        raise  
    except Exception as e:
        logger.error(f"Error updating service {service_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Aktualisieren des Services."
        )

@router.delete("/{service_id}")
async def delete_service(service_id: str):
    """
    Delete a service (admin only).
    """
    try:
        result = await db.services.delete_one({"id": service_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service nicht gefunden."
            )
        
        logger.info(f"Service deleted: {service_id}")
        return {"success": True, "message": "Service erfolgreich gelöscht."}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting service {service_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fehler beim Löschen des Services."
        )