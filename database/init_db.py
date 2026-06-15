"""Updated database initialization script with materials catalog"""
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DevelopmentConfig
from database import db, init_db
from database.models import Customer, Material, Quotation, QuotationItem, Invoice, Inventory, AIQuotationLog
from app.services.materials_catalog_service import MaterialsCatalogService
from flask import Flask

def seed_database():
    """Seed the database with sample data"""
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    init_db(app)
    
    with app.app_context():
        # Check if data already exists
        if Customer.query.first() is not None:
            print("Database already seeded. Skipping...")
            return
        
        # Add sample customers
        customers = [
            Customer(
                name="Rajesh Kumar",
                email="rajesh@example.com",
                phone="+91-9876543210",
                address="123 Main Street",
                city="Mumbai",
                state="Maharashtra",
                postal_code="400001",
                country="India",
                company="Kumar Constructions",
                gst_number="27ABCDE1234F1Z0"
            ),
            Customer(
                name="Priya Patel",
                email="priya@example.com",
                phone="+91-9876543211",
                address="456 Oak Avenue",
                city="Bangalore",
                state="Karnataka",
                postal_code="560001",
                country="India",
                company="Patel Interiors",
                gst_number="29ABCDE1234F1Z0"
            ),
        ]
        
        # Add to session and commit
        for customer in customers:
            db.session.add(customer)
        
        db.session.commit()
        
        # Seed marble materials
        print("\n📦 Seeding marble materials...")
        marble_count = MaterialsCatalogService.seed_marble_materials()
        print(f"✅ Added {marble_count} marble materials")
        
        # Seed porcelain materials
        print("\n📦 Seeding porcelain materials...")
        porcelain_count = MaterialsCatalogService.seed_porcelain_materials()
        print(f"✅ Added {porcelain_count} porcelain materials")
        
        print("""
✅ Database seeded successfully!
   - Created {0} customers
   - Created {1} marble materials
   - Created {2} porcelain materials
   - Total materials: {3}
        """.format(len(customers), marble_count, porcelain_count, marble_count + porcelain_count))

if __name__ == "__main__":
    seed_database()
