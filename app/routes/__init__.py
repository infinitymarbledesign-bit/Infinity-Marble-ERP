"""Routes module"""
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from app.routes import customers, materials, quotations, invoices, ai_quotations

# Register sub-blueprints
api_bp.register_blueprint(customers.customers_bp)
api_bp.register_blueprint(materials.materials_bp)
api_bp.register_blueprint(quotations.quotations_bp)
api_bp.register_blueprint(invoices.invoices_bp)
api_bp.register_blueprint(ai_quotations.ai_bp)
