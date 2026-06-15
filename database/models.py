"""Database models for Infinity Marble ERP"""
from database import db
from datetime import datetime
from sqlalchemy import Index

class Customer(db.Model):
    """Customer model for storing customer information"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(255), nullable=True)
    gst_number = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    quotations = db.relationship('Quotation', backref='customer', lazy=True, cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', backref='customer', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_customer_email', 'email'),
        Index('idx_customer_name', 'name'),
    )
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Material(db.Model):
    """Material model for storing marble and porcelain information"""
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    material_type = db.Column(db.String(50), nullable=False)  # 'marble' or 'porcelain'
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(100), nullable=True)
    finish = db.Column(db.String(100), nullable=True)  # polished, honed, brushed, etc.
    price_per_sqft = db.Column(db.Float, nullable=False)
    price_per_meter = db.Column(db.Float, nullable=True)
    density = db.Column(db.Float, nullable=True)  # kg/m³
    mohs_hardness = db.Column(db.Float, nullable=True)  # For durability
    origin = db.Column(db.String(100), nullable=True)
    supplier = db.Column(db.String(255), nullable=True)
    stock_quantity = db.Column(db.Float, default=0)  # In square feet
    reorder_level = db.Column(db.Float, default=100)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    quotation_items = db.relationship('QuotationItem', backref='material', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_material_code', 'code'),
        Index('idx_material_type', 'material_type'),
    )
    
    def __repr__(self):
        return f'<Material {self.name}>'

class Quotation(db.Model):
    """Quotation model for storing quotation details"""
    __tablename__ = 'quotations'
    
    id = db.Column(db.Integer, primary_key=True)
    quotation_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subtotal = db.Column(db.Float, default=0)
    tax_percentage = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    discount_percentage = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='draft')  # draft, sent, accepted, rejected, invoiced
    validity_days = db.Column(db.Integer, default=30)
    notes = db.Column(db.Text, nullable=True)
    ai_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    items = db.relationship('QuotationItem', backref='quotation', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        Index('idx_quotation_number', 'quotation_number'),
        Index('idx_quotation_customer', 'customer_id'),
        Index('idx_quotation_status', 'status'),
    )
    
    def __repr__(self):
        return f'<Quotation {self.quotation_number}>'

class QuotationItem(db.Model):
    """Quotation Item model for line items in quotations"""
    __tablename__ = 'quotation_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # in square feet or meters
    unit = db.Column(db.String(20), default='sqft')  # sqft, meter, piece
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    __table_args__ = (
        Index('idx_quotation_item_quotation', 'quotation_id'),
        Index('idx_quotation_item_material', 'material_id'),
    )
    
    def __repr__(self):
        return f'<QuotationItem {self.id}>'

class Invoice(db.Model):
    """Invoice model for storing invoice details"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    subtotal = db.Column(db.Float, default=0)
    tax_percentage = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    discount_percentage = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, default=0)
    payment_status = db.Column(db.String(50), default='pending')  # pending, partial, paid
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_invoice_number', 'invoice_number'),
        Index('idx_invoice_customer', 'customer_id'),
        Index('idx_invoice_status', 'payment_status'),
    )
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'

class Inventory(db.Model):
    """Inventory model for tracking stock movements"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # in, out, adjustment
    quantity = db.Column(db.Float, nullable=False)
    reference_id = db.Column(db.String(100), nullable=True)  # Quotation or PO number
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=True)
    
    __table_args__ = (
        Index('idx_inventory_material', 'material_id'),
        Index('idx_inventory_type', 'transaction_type'),
    )
    
    def __repr__(self):
        return f'<Inventory {self.id}>'

class AIQuotationLog(db.Model):
    """AI Quotation Log model for tracking AI-generated quotations"""
    __tablename__ = 'ai_quotation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    ai_model = db.Column(db.String(100), nullable=False)  # openai, ai21, etc.
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    processing_time = db.Column(db.Float, nullable=True)  # in seconds
    tokens_used = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_ai_quotation_log_quotation', 'quotation_id'),
    )
    
    def __repr__(self):
        return f'<AIQuotationLog {self.id}>'
