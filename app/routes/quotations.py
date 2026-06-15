"""Quotation routes"""
from flask import Blueprint, request, jsonify
from database import db
from database.models import Quotation, QuotationItem, Customer, Material
from datetime import datetime

quotations_bp = Blueprint('quotations', __name__, url_prefix='/quotations')

@quotations_bp.route('', methods=['GET'])
def get_quotations():
    """Get all quotations"""
    customer_id = request.args.get('customer_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Quotation.query
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    quotations = [{
        'id': q.id,
        'quotation_number': q.quotation_number,
        'customer_name': q.customer.name,
        'total_amount': q.total_amount,
        'status': q.status,
        'created_at': q.created_at.isoformat()
    } for q in pagination.items]
    
    return jsonify({
        'data': quotations,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@quotations_bp.route('/<int:quotation_id>', methods=['GET'])
def get_quotation(quotation_id):
    """Get quotation by ID"""
    quotation = Quotation.query.get_or_404(quotation_id)
    
    items = [{
        'id': item.id,
        'material_id': item.material_id,
        'material_name': item.material.name,
        'quantity': item.quantity,
        'unit': item.unit,
        'unit_price': item.unit_price,
        'line_total': item.line_total
    } for item in quotation.items]
    
    return jsonify({
        'id': quotation.id,
        'quotation_number': quotation.quotation_number,
        'customer_id': quotation.customer_id,
        'customer_name': quotation.customer.name,
        'title': quotation.title,
        'description': quotation.description,
        'items': items,
        'subtotal': quotation.subtotal,
        'tax_percentage': quotation.tax_percentage,
        'tax_amount': quotation.tax_amount,
        'discount_percentage': quotation.discount_percentage,
        'discount_amount': quotation.discount_amount,
        'total_amount': quotation.total_amount,
        'status': quotation.status,
        'ai_generated': quotation.ai_generated,
        'created_at': quotation.created_at.isoformat()
    })

@quotations_bp.route('', methods=['POST'])
def create_quotation():
    """Create new quotation"""
    data = request.get_json()
    
    try:
        # Generate quotation number
        last_quotation = Quotation.query.order_by(Quotation.id.desc()).first()
        quotation_number = f"QT-{datetime.now().strftime('%Y%m%d')}-{(last_quotation.id if last_quotation else 0) + 1:04d}"
        
        quotation = Quotation(
            quotation_number=quotation_number,
            customer_id=data.get('customer_id'),
            title=data.get('title'),
            description=data.get('description'),
            tax_percentage=data.get('tax_percentage', 0),
            discount_percentage=data.get('discount_percentage', 0)
        )
        
        db.session.add(quotation)
        db.session.flush()
        
        # Add items
        total = 0
        for item_data in data.get('items', []):
            material = Material.query.get(item_data['material_id'])
            if not material:
                raise ValueError(f"Material {item_data['material_id']} not found")
            
            line_total = item_data['quantity'] * item_data['unit_price']
            item = QuotationItem(
                quotation_id=quotation.id,
                material_id=item_data['material_id'],
                quantity=item_data['quantity'],
                unit=item_data.get('unit', 'sqft'),
                unit_price=item_data['unit_price'],
                line_total=line_total
            )
            db.session.add(item)
            total += line_total
        
        # Calculate totals
        quotation.subtotal = total
        quotation.tax_amount = total * (quotation.tax_percentage / 100)
        quotation.discount_amount = total * (quotation.discount_percentage / 100)
        quotation.total_amount = total + quotation.tax_amount - quotation.discount_amount
        
        db.session.commit()
        
        return jsonify({
            'id': quotation.id,
            'quotation_number': quotation.quotation_number,
            'message': 'Quotation created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
