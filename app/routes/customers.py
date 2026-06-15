"""Customer routes"""
from flask import Blueprint, request, jsonify
from database import db
from database.models import Customer
from sqlalchemy.exc import IntegrityError

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('', methods=['GET'])
def get_customers():
    """Get all customers"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Customer.query.filter_by(is_active=True)
    pagination = query.paginate(page=page, per_page=per_page)
    
    customers = [{
        'id': c.id,
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'company': c.company,
        'city': c.city,
        'created_at': c.created_at.isoformat()
    } for c in pagination.items]
    
    return jsonify({
        'data': customers,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get customer by ID"""
    customer = Customer.query.get_or_404(customer_id)
    
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address,
        'city': customer.city,
        'state': customer.state,
        'postal_code': customer.postal_code,
        'country': customer.country,
        'company': customer.company,
        'gst_number': customer.gst_number,
        'created_at': customer.created_at.isoformat(),
        'updated_at': customer.updated_at.isoformat()
    })

@customers_bp.route('', methods=['POST'])
def create_customer():
    """Create new customer"""
    data = request.get_json()
    
    try:
        customer = Customer(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country'),
            company=data.get('company'),
            gst_number=data.get('gst_number')
        )
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({'id': customer.id, 'message': 'Customer created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update customer"""
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if hasattr(customer, key) and key not in ['id', 'created_at']:
                setattr(customer, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
