# Infinity Marble ERP - Setup Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/infinitymarbledesign-bit/Infinity-Marble-ERP.git
cd Infinity-Marble-ERP

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys and settings
# Important: Add your OpenAI and AI21 API keys
```

### 3. Database Setup

```bash
# Initialize and seed the database
python database/init_db.py
```

### 4. Run the Application

```bash
# Development server
python main.py

# The API will be available at: http://localhost:5000
```

## Project Structure

```
Infinity-Marble-ERP/
├── app/                    # Flask application
│   ├── routes/            # API endpoints
│   │   ├── customers.py   # Customer management
│   │   ├── materials.py   # Material management
│   │   ├── quotations.py  # Quotation management
│   │   ├── invoices.py    # Invoice management
│   │   └── ai_quotations.py  # AI-powered quotations
│   └── __init__.py
├── database/              # Database layer
│   ├── models.py         # SQLAlchemy models
│   ├── init_db.py        # Database initialization
│   └── marble.db         # SQLite database (created after init)
├── config.py             # Configuration management
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README_SETUP.md       # This file
```

## Database Models

### Customer
- Stores customer information
- Fields: name, email, phone, address, GST number, etc.
- Relationships: quotations, invoices

### Material
- Marble and porcelain information
- Fields: name, type, color, finish, price, stock, etc.
- Relationships: quotation items

### Quotation
- Quotation details
- Fields: quotation number, customer, items, total, status, etc.
- Relationships: customer, items, invoices

### QuotationItem
- Line items in quotations
- Fields: material, quantity, unit price, line total

### Invoice
- Invoice details
- Fields: invoice number, customer, amount, payment status

### Inventory
- Stock tracking and movements
- Fields: material, transaction type, quantity, notes

### AIQuotationLog
- Log of AI-generated quotations
- Fields: quotation, AI model, prompt, response, tokens used

## API Endpoints

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/<id>` - Get customer details
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer

### Materials
- `GET /api/materials` - List all materials
- `GET /api/materials/<id>` - Get material details
- `POST /api/materials` - Create new material

### Quotations
- `GET /api/quotations` - List all quotations
- `GET /api/quotations/<id>` - Get quotation details
- `POST /api/quotations` - Create new quotation

### AI Quotations
- `POST /api/ai/quotation` - Generate quotation using AI
- `POST /api/ai/quotation/<id>/suggest` - Get material suggestions

## Development

### Testing

```bash
python -m pytest
```

### Code Style

```bash
# Format code
python -m black .

# Lint
python -m flake8 .
```

## Features Roadmap

- [x] Database schema and models
- [x] Basic REST API
- [ ] AI quotation generation (OpenAI/AI21)
- [ ] PDF/Excel/Word export
- [ ] Email integration
- [ ] Payment gateway integration
- [ ] Frontend UI (React/Vue)
- [ ] Mobile app
- [ ] Advanced analytics and reporting

## Support

For issues, questions, or contributions, please visit:
https://github.com/infinitymarbledesign-bit/Infinity-Marble-ERP
