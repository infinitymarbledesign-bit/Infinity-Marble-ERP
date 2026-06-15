"""Updated AI quotation routes with AI service integration"""
from flask import Blueprint, request, jsonify
from database import db
from database.models import Quotation, AIQuotationLog
from app.services.ai_service import AIQuotationService
import os

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')
ai_service = AIQuotationService()

@ai_bp.route('/quotation/generate', methods=['POST'])
def generate_quotation():
    """Generate quotation using AI"""
    data = request.get_json()
    
    try:
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({
                'error': 'OpenAI API key not configured',
                'hint': 'Add OPENAI_API_KEY to .env file'
            }), 400
        
        customer_id = data.get('customer_id')
        requirements = data.get('requirements')
        model = data.get('model', 'gpt-3.5-turbo')
        
        if not customer_id or not requirements:
            return jsonify({'error': 'customer_id and requirements are required'}), 400
        
        quotation_id = ai_service.generate_quotation(customer_id, requirements, model)
        
        return jsonify({
            'quotation_id': quotation_id,
            'message': 'AI quotation generated successfully'
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ai_bp.route('/quotation/<int:quotation_id>/suggest', methods=['POST'])
def suggest_materials(quotation_id):
    """Suggest materials for a quotation using AI"""
    data = request.get_json() or {}
    
    try:
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({
                'error': 'OpenAI API key not configured',
                'hint': 'Add OPENAI_API_KEY to .env file'
            }), 400
        
        quotation = Quotation.query.get_or_404(quotation_id)
        preferences = data.get('preferences')
        model = data.get('model', 'gpt-3.5-turbo')
        
        suggestions = ai_service.suggest_materials(quotation_id, preferences, model)
        
        return jsonify(suggestions)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@ai_bp.route('/estimate-cost', methods=['POST'])
def estimate_cost():
    """Estimate project cost using AI"""
    data = request.get_json()
    
    try:
        if not os.getenv('OPENAI_API_KEY'):
            return jsonify({
                'error': 'OpenAI API key not configured',
                'hint': 'Add OPENAI_API_KEY to .env file'
            }), 400
        
        area = data.get('area')
        material_type = data.get('material_type')
        finish = data.get('finish')
        labor_rate = data.get('labor_rate')
        
        if not all([area, material_type, finish]):
            return jsonify({'error': 'area, material_type, and finish are required'}), 400
        
        cost_breakdown = ai_service.estimate_project_cost(
            area, material_type, finish, labor_rate
        )
        
        return jsonify(cost_breakdown)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
