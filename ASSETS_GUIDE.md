# Infinity Marble ERP - Assets Guide

## Logo Placement
- **File:** `assets/logo/company_logo.png`
- **Usage:** Displayed on invoices, quotations, and letterheads
- **Recommended Size:** 1000x1000px
- **Format:** PNG with transparency

## Letterhead
- **File:** `assets/letterhead/letterhead.png`
- **Usage:** Header for invoices and official documents
- **Recommended Size:** 2100x300px (7" x 1" at 300 DPI)
- **Format:** PNG with company branding

## Stamp
- **File:** `assets/stamp/company_stamp.png`
- **Usage:** Document authorization
- **Recommended Size:** 500x500px
- **Format:** PNG with transparency

## Signature
- **File:** `assets/signature/authorized_signature.png`
- **Usage:** Invoice signing
- **Recommended Size:** 400x200px
- **Format:** PNG with transparency

## Adding Your Assets

### Steps:
1. Create the folder structure:
   ```bash
   mkdir -p assets/logo
   mkdir -p assets/letterhead
   mkdir -p assets/stamp
   mkdir -p assets/signature
   ```

2. Place your files:
   ```bash
   cp /path/to/your/logo.png assets/logo/company_logo.png
   cp /path/to/your/letterhead.png assets/letterhead/letterhead.png
   cp /path/to/your/stamp.png assets/stamp/company_stamp.png
   cp /path/to/your/signature.png assets/signature/authorized_signature.png
   ```

3. The system will automatically use these images in generated documents

## Design Recommendations

### Company Logo
- Use high-resolution PNG format
- Include transparent background
- Keep aspect ratio 1:1 (square)
- Minimum 200x200px, recommended 1000x1000px

### Letterhead
- Professional header design
- Include company name, contact info
- Recommended resolution: 2100x300px
- Can include subtle background pattern

### Stamp
- Circular design preferred
- Include company name or authority
- High contrast for visibility

### Signature
- Professional signature image
- Clear and legible
- Transparent background recommended

## File Organization

```
assets/
├── logo/
│   └── company_logo.png
├── letterhead/
│   └── letterhead.png
├── stamp/
│   └── company_stamp.png
└── signature/
    └── authorized_signature.png
```

## Usage in Code

The invoice service automatically includes these assets:

```python
from app.services.invoice_service import InvoiceService

service = InvoiceService()
pdf = service.export_invoice_pdf(invoice_id)
```

The logo and letterhead are automatically embedded in generated PDFs.
