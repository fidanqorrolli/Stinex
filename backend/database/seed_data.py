"""
Seed script to populate the database with initial data for Stinex cleaning service.
This script creates sample services and testimonials.
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def seed_services():
    """Seed the database with initial services."""
    services = [
        {
            "id": str(uuid.uuid4()),
            "title": "Büroreinigung",
            "description": "Professionelle Reinigung für Büros, Praxen und Verwaltungsgebäude",
            "pricing": "Ab 15€ pro Stunde",
            "features": [
                "Tägliche oder wöchentliche Reinigung",
                "Schreibtische und Arbeitsflächen",
                "Sanitäranlagen und Küchen",
                "Staubsaugen und Wischen",
                "Fensterreinigung",
                "Müllentsorgung"
            ],
            "category": "commercial",
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Wohnungsreinigung",
            "description": "Gründliche Reinigung für Ihr Zuhause - von der Grundreinigung bis zur regelmäßigen Pflege",
            "pricing": "Ab 25€ pro Stunde",
            "features": [
                "Grundreinigung bei Umzug",
                "Regelmäßige Haushaltsreinigung",
                "Bad- und Küchenreinigung",
                "Fenster innen und außen",
                "Treppenhaus reinigen",
                "Balkon und Terrasse"
            ],
            "category": "residential",
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Gewerbereinigung",
            "description": "Spezialisierte Reinigung für Geschäfte, Restaurants und Industrieobjekte",
            "pricing": "Individuell kalkuliert",
            "features": [
                "Ladenlokale und Geschäfte",
                "Restaurants und Cafés",
                "Lagerhallen und Werkstätten",
                "Hotelreinigung",
                "Praxen und Kliniken",
                "Industriereinigung"
            ],
            "category": "industrial",
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Check if services already exist
    existing_count = await db.services.count_documents({})
    if existing_count == 0:
        await db.services.insert_many(services)
        print(f"✅ Inserted {len(services)} services")
    else:
        print(f"⚠️ Services already exist ({existing_count} documents)")

async def seed_testimonials():
    """Seed the database with initial testimonials."""
    testimonials = [
        {
            "id": str(uuid.uuid4()),
            "name": "Maria Schmidt",
            "company": "Schmidt & Partner",
            "text": "Stinex reinigt unsere Büroräume seit 2 Jahren. Immer zuverlässig und gründlich!",
            "rating": 5,
            "approved": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Thomas Weber",
            "company": "Weber Immobilien",
            "text": "Hervorragender Service! Die Qualität stimmt und das Team ist sehr professionell.",
            "rating": 5,
            "approved": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Anna Müller",
            "company": "Privatkundin",
            "text": "Endlich eine Reinigungsfirma, die hält, was sie verspricht. Sehr empfehlenswert!",
            "rating": 5,
            "approved": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Peter Krause",
            "company": "Krause GmbH",
            "text": "Professionelle Zusammenarbeit und faire Preise. Wir sind sehr zufrieden.",
            "rating": 5,
            "approved": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Lisa Hofmann",
            "company": "Privatkundin",
            "text": "Schnell, zuverlässig und gründlich. Kann Stinex nur weiterempfehlen!",
            "rating": 5,
            "approved": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Check if testimonials already exist
    existing_count = await db.testimonials.count_documents({})
    if existing_count == 0:
        await db.testimonials.insert_many(testimonials)
        print(f"✅ Inserted {len(testimonials)} testimonials")
    else:
        print(f"⚠️ Testimonials already exist ({existing_count} documents)")

async def create_indexes():
    """Create database indexes for better performance."""
    # Create indexes for contacts
    await db.contacts.create_index("created_at")
    await db.contacts.create_index("status")
    await db.contacts.create_index("email")
    
    # Create indexes for services
    await db.services.create_index("active")
    await db.services.create_index("category")
    
    # Create indexes for testimonials
    await db.testimonials.create_index("approved")
    await db.testimonials.create_index("rating")
    
    print("✅ Database indexes created")

async def seed_database():
    """Main seeding function."""
    print("🌱 Starting database seeding...")
    
    try:
        await seed_services()
        await seed_testimonials() 
        await create_indexes()
        print("🎉 Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())