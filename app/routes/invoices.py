"""Invoice routes"""
from flask import Blueprint, request, jsonify
from database import db
from database.models import Invoice
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('', methods=['GET'])
def get_invoices():
    """Get all invoices"""
    customer_id = request.args.get('customer_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Invoice.query
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if status:
        query = query.filter_by(payment_status=status)
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    invoices = [{
        'id': i.id,
        'invoice_number': i.invoice_number,
        'customer_name': i.customer.name,
        'total_amount': i.total_amount,
        'payment_status': i.payment_status,
        'created_at': i.created_at.isoformat()
    } for i in pagination.items]
    
    return jsonify({
        'data': invoices,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@invoices_bp.route('/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get invoice by ID"""
    invoice = Invoice.query.get_or_404(invoice_id)
    
    return jsonify({
        'id': invoice.id,
        'invoice_number': invoice.invoice_number,
        'customer_id': invoice.customer_id,
        'customer_name': invoice.customer.name,
        'subtotal': invoice.subtotal,
        'tax_amount': invoice.tax_amount,
        'discount_amount': invoice.discount_amount,
        'total_amount': invoice.total_amount,
        'payment_status': invoice.payment_status,
        'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
        'created_at': invoice.created_at.isoformat()
    })
