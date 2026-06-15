"""Material routes"""
from flask import Blueprint, request, jsonify
from database import db
from database.models import Material

materials_bp = Blueprint('materials', __name__, url_prefix='/materials')

@materials_bp.route('', methods=['GET'])
def get_materials():
    """Get all materials"""
    material_type = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Material.query.filter_by(is_active=True)
    if material_type:
        query = query.filter_by(material_type=material_type)
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    materials = [{
        'id': m.id,
        'name': m.name,
        'material_type': m.material_type,
        'code': m.code,
        'color': m.color,
        'price_per_sqft': m.price_per_sqft,
        'stock_quantity': m.stock_quantity
    } for m in pagination.items]
    
    return jsonify({
        'data': materials,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@materials_bp.route('/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """Get material by ID"""
    material = Material.query.get_or_404(material_id)
    
    return jsonify({
        'id': material.id,
        'name': material.name,
        'material_type': material.material_type,
        'code': material.code,
        'description': material.description,
        'color': material.color,
        'finish': material.finish,
        'price_per_sqft': material.price_per_sqft,
        'price_per_meter': material.price_per_meter,
        'density': material.density,
        'mohs_hardness': material.mohs_hardness,
        'origin': material.origin,
        'supplier': material.supplier,
        'stock_quantity': material.stock_quantity,
        'reorder_level': material.reorder_level,
        'created_at': material.created_at.isoformat()
    })

@materials_bp.route('', methods=['POST'])
def create_material():
    """Create new material"""
    data = request.get_json()
    
    try:
        material = Material(
            name=data.get('name'),
            material_type=data.get('material_type'),
            code=data.get('code'),
            description=data.get('description'),
            color=data.get('color'),
            finish=data.get('finish'),
            price_per_sqft=data.get('price_per_sqft'),
            price_per_meter=data.get('price_per_meter'),
            density=data.get('density'),
            mohs_hardness=data.get('mohs_hardness'),
            origin=data.get('origin'),
            supplier=data.get('supplier'),
            stock_quantity=data.get('stock_quantity', 0)
        )
        db.session.add(material)
        db.session.commit()
        
        return jsonify({'id': material.id, 'message': 'Material created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
