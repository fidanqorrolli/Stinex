from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

# Import route modules
from routes.contact import router as contact_router
from routes.services import router as services_router  
from routes.testimonials import router as testimonials_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.info("🚀 Starting Stinex Backend Server...")
    
    # Test database connection
    try:
        await client.admin.command('ping')
        logging.info("✅ MongoDB connection successful")
    except Exception as e:
        logging.error(f"❌ MongoDB connection failed: {e}")
        raise
    
    # Run database seeding if needed
    try:
        from database.seed_data import seed_database
        # Only seed if collections are empty
        contacts_count = await db.contacts.count_documents({})
        services_count = await db.services.count_documents({})
        testimonials_count = await db.testimonials.count_documents({})
        
        if services_count == 0 or testimonials_count == 0:
            logging.info("🌱 Seeding database with initial data...")
            await seed_database()
    except Exception as e:
        logging.warning(f"⚠️ Database seeding failed (continuing anyway): {e}")
    
    yield
    
    # Shutdown
    logging.info("🛑 Shutting down Stinex Backend Server...")
    client.close()

# Create the main app with lifespan
app = FastAPI(
    title="Stinex Cleaning Service API",
    description="Backend API for Stinex cleaning service website",
    version="1.0.0",
    lifespan=lifespan
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Stinex API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@api_router.get("/health")
async def health_check():
    try:
        # Test database connection
        await client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2025-01-28T21:45:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

# Include all route modules
api_router.include_router(contact_router)
api_router.include_router(services_router)
api_router.include_router(testimonials_router)

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # In production, specify exact origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "success": False,
        "error": "http_error",
        "message": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "success": False,
        "error": "internal_error",
        "message": "Ein unerwarteter Fehler ist aufgetreten.",
        "status_code": 500
    }