"""Invoice Service with printer support"""
import os
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from database.models import Invoice

class InvoiceService:
    """Service for generating and printing invoices"""
    
    def __init__(self):
        self.logo_path = 'assets/logo/company_logo.png'
        self.letterhead_path = 'assets/letterhead/letterhead.png'
    
    def export_invoice_pdf(self, invoice_id, print_format=False):
        """
        Export invoice as PDF
        
        Args:
            invoice_id: ID of invoice to export
            print_format: If True, optimize for printing
        
        Returns:
            PDF file bytes
        """
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Create PDF
        buffer = BytesIO()
        pagesize = A4 if print_format else letter
        doc = SimpleDocTemplate(buffer, pagesize=pagesize, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Add custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=1  # Center
        )
        
        # Add letterhead if available
        if os.path.exists(self.letterhead_path):
            try:
                letterhead = Image(self.letterhead_path, width=7*inch, height=1*inch)
                elements.append(letterhead)
                elements.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Add logo if available
        if os.path.exists(self.logo_path):
            try:
                logo = Image(self.logo_path, width=1*inch, height=1*inch)
                elements.append(logo)
            except:
                pass
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Title
        title = Paragraph("<b>INVOICE</b>", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Invoice details
        details_data = [
            ['Invoice Number:', invoice.invoice_number, 'Date:', invoice.created_at.strftime('%Y-%m-%d')],
            ['Payment Status:', invoice.payment_status.upper(), 'Due Date:', invoice.due_date.strftime('%Y-%m-%d') if invoice.due_date else 'N/A'],
        ]
        
        details_table = Table(details_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Customer info
        elements.append(Paragraph("<b>Bill To:</b>", styles['Heading3']))
        customer_info = f"""
        {invoice.customer.name}<br/>
        {invoice.customer.company}<br/>
        {invoice.customer.address}<br/>
        {invoice.customer.city}, {invoice.customer.state} {invoice.customer.postal_code}<br/>
        {invoice.customer.email}<br/>
        {invoice.customer.phone}
        """
        elements.append(Paragraph(customer_info, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Items table (if invoice has related quotation)
        if invoice.quotation_id:
            quotation = invoice.quotation
            items_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
            
            for item in quotation.items:
                items_data.append([
                    item.material.name,
                    f"{item.quantity}",
                    f"${item.unit_price:.2f}",
                    f"${item.line_total:.2f}"
                ])
            
            items_table = Table(items_data)
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ]))
            elements.append(items_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Totals section
        totals_data = [
            ['', '', 'Subtotal:', f"${invoice.subtotal:.2f}"],
            ['', '', f'Tax ({invoice.tax_percentage}%):', f"${invoice.tax_amount:.2f}"],
            ['', '', 'Discount:', f"-${invoice.discount_amount:.2f}"],
            ['', '', 'TOTAL:', f"${invoice.total_amount:.2f}"],
        ]
        
        totals_table = Table(totals_data, colWidths=[2*inch, 2*inch, 1.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (2, 0), (-1, 2), 'Helvetica'),
            ('FONTNAME', (2, 3), (-1, 3), 'Helvetica-Bold'),
            ('FONTSIZE', (2, 3), (-1, 3), 12),
            ('BACKGROUND', (2, 3), (-1, 3), colors.HexColor('#D3D3D3')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Payment instructions
        elements.append(Paragraph("<b>Payment Instructions:</b>", styles['Heading3']))
        payment_info = """
        Please make payment within 30 days of invoice date. <br/>
        Bank Details: [Your Bank Details]<br/>
        UPI: [Your UPI ID]<br/>
        GST Number: [Your GST Number]
        """
        elements.append(Paragraph(payment_info, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer = Paragraph(
            "<i>Thank you for your business! This is an electronically generated invoice.</i>",
            ParagraphStyle('Footer', parent=styles['Normal'], alignment=1, fontSize=8, textColor=colors.grey)
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return buffer.getvalue()
