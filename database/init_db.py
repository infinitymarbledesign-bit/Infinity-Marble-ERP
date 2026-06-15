"""Database initialization script"""
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DevelopmentConfig
from database import db, init_db
from database.models import Customer, Material, Quotation, QuotationItem, Invoice, Inventory, AIQuotationLog
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
        
        # Add sample materials
        materials = [
            Material(
                name="Italian Carrara Marble",
                material_type="marble",
                code="MAR-001",
                description="Premium white Carrara marble from Italy",
                color="White",
                finish="Polished",
                price_per_sqft=15.50,
                price_per_meter=166.80,
                density=2700,
                mohs_hardness=3.0,
                origin="Carrara, Italy",
                supplier="Italian Marble Imports",
                stock_quantity=500
            ),
            Material(
                name="Black Galaxy Granite",
                material_type="marble",
                code="MAR-002",
                description="Elegant black granite with golden flecks",
                color="Black",
                finish="Polished",
                price_per_sqft=12.00,
                price_per_meter=129.17,
                density=2750,
                mohs_hardness=7.0,
                origin="India",
                supplier="Galaxy Granite Works",
                stock_quantity=750
            ),
            Material(
                name="Ceramic Porcelain Tile",
                material_type="porcelain",
                code="POR-001",
                description="High-quality ceramic porcelain tiles",
                color="Cream",
                finish="Matte",
                price_per_sqft=8.50,
                price_per_meter=91.49,
                density=2400,
                mohs_hardness=8.0,
                origin="China",
                supplier="Premium Ceramics Ltd",
                stock_quantity=1000
            ),
        ]
        
        # Add to session and commit
        for customer in customers:
            db.session.add(customer)
        for material in materials:
            db.session.add(material)
        
        db.session.commit()
        print("✅ Database seeded successfully!")
        print(f"   - Created {len(customers)} customers")
        print(f"   - Created {len(materials)} materials")

if __name__ == "__main__":
    seed_database()
