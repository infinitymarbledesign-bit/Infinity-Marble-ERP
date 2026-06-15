"""Export routes"""
from flask import Blueprint, send_file, request, jsonify
from app.services.export_service import ExportService
from database.models import Quotation, Invoice

export_bp = Blueprint('export', __name__, url_prefix='/export')

@export_bp.route('/quotation/<int:quotation_id>/pdf', methods=['GET'])
def export_quotation_pdf(quotation_id):
    """Export quotation as PDF"""
    try:
        pdf_bytes = ExportService.export_quotation_pdf(quotation_id)
        return send_file(
            pdf_bytes,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'quotation_{quotation_id}.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@export_bp.route('/quotation/<int:quotation_id>/excel', methods=['GET'])
def export_quotation_excel(quotation_id):
    """Export quotation as Excel"""
    try:
        excel_bytes = ExportService.export_quotation_excel(quotation_id)
        return send_file(
            excel_bytes,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'quotation_{quotation_id}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@export_bp.route('/quotation/<int:quotation_id>/word', methods=['GET'])
def export_quotation_word(quotation_id):
    """Export quotation as Word document"""
    try:
        word_bytes = ExportService.export_quotation_word(quotation_id)
        return send_file(
            word_bytes,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f'quotation_{quotation_id}.docx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
