"""Updated Invoice routes with printer support"""
from flask import Blueprint, request, jsonify, send_file
from database import db
from database.models import Invoice, Quotation
from app.services.export_service import ExportService
from app.services.invoice_service import InvoiceService
from datetime import datetime, timedelta

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')
invoice_service = InvoiceService()

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

@invoices_bp.route('/quotation/<int:quotation_id>/create', methods=['POST'])
def create_invoice_from_quotation(quotation_id):
    """Create invoice from quotation"""
    try:
        quotation = Quotation.query.get_or_404(quotation_id)
        
        # Generate invoice number
        last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{(last_invoice.id if last_invoice else 0) + 1:04d}"
        
        # Create invoice from quotation
        invoice = Invoice(
            invoice_number=invoice_number,
            quotation_id=quotation_id,
            customer_id=quotation.customer_id,
            subtotal=quotation.subtotal,
            tax_percentage=quotation.tax_percentage,
            tax_amount=quotation.tax_amount,
            discount_percentage=quotation.discount_percentage,
            discount_amount=quotation.discount_amount,
            total_amount=quotation.total_amount,
            due_date=datetime.utcnow() + timedelta(days=30),
            payment_status='pending'
        )
        
        db.session.add(invoice)
        quotation.status = 'invoiced'
        db.session.commit()
        
        return jsonify({
            'id': invoice.id,
            'invoice_number': invoice_number,
            'message': 'Invoice created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/<int:invoice_id>/pdf', methods=['GET'])
def export_invoice_pdf(invoice_id):
    """Export invoice as PDF"""
    try:
        pdf_bytes = invoice_service.export_invoice_pdf(invoice_id)
        return send_file(
            pdf_bytes,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'invoice_{invoice_id}.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/<int:invoice_id>/print', methods=['GET'])
def print_invoice(invoice_id):
    """Print invoice (returns PDF optimized for printing)"""
    try:
        pdf_bytes = invoice_service.export_invoice_pdf(invoice_id, print_format=True)
        return send_file(
            pdf_bytes,
            mimetype='application/pdf',
            download_name=f'invoice_{invoice_id}_print.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/<int:invoice_id>/mark-paid', methods=['PUT'])
def mark_invoice_paid(invoice_id):
    """Mark invoice as paid"""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        invoice.payment_status = 'paid'
        db.session.commit()
        
        return jsonify({'message': 'Invoice marked as paid'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
