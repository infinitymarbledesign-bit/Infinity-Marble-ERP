"""Comprehensive project API documentation"""

# Infinity Marble ERP - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API is open. Add authentication headers as needed.

## Endpoints

### Customers

#### Get All Customers
```http
GET /customers?page=1&per_page=20
```
**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-234-567-8900",
      "company": "ABC Corp",
      "city": "New York",
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 10,
  "pages": 1,
  "current_page": 1
}
```

#### Get Customer by ID
```http
GET /customers/{id}
```

#### Create Customer
```http
POST /customers
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "company": "ABC Corp",
  "city": "New York",
  "state": "NY",
  "postal_code": "10001",
  "country": "USA",
  "gst_number": "12345678901234"
}
```

#### Update Customer
```http
PUT /customers/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "email": "newemail@example.com"
}
```

---

### Materials

#### Get All Materials
```http
GET /materials?type=marble&page=1&per_page=20
```
**Query Parameters:**
- `type`: 'marble' or 'porcelain' (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

#### Get Material by ID
```http
GET /materials/{id}
```

#### Create Material
```http
POST /materials
Content-Type: application/json

{
  "name": "Italian Marble",
  "material_type": "marble",
  "code": "MAR-001",
  "color": "White",
  "finish": "Polished",
  "price_per_sqft": 15.50,
  "origin": "Italy",
  "supplier": "Italian Imports",
  "stock_quantity": 500
}
```

---

### Quotations

#### Get All Quotations
```http
GET /quotations?customer_id=1&status=draft&page=1&per_page=20
```
**Query Parameters:**
- `customer_id`: Filter by customer (optional)
- `status`: Filter by status - draft, sent, accepted, rejected, invoiced (optional)
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)

#### Get Quotation by ID
```http
GET /quotations/{id}
```

#### Create Quotation
```http
POST /quotations
Content-Type: application/json

{
  "customer_id": 1,
  "title": "Kitchen Countertop",
  "description": "High-quality marble countertop",
  "tax_percentage": 10,
  "discount_percentage": 5,
  "items": [
    {
      "material_id": 1,
      "quantity": 50,
      "unit": "sqft",
      "unit_price": 15.50
    }
  ]
}
```

---

### AI Quotations

#### Generate AI Quotation
```http
POST /ai/quotation/generate
Content-Type: application/json

{
  "customer_id": 1,
  "requirements": {
    "project_type": "Kitchen Countertop",
    "area": 100,
    "finish": "polished",
    "budget": 5000,
    "description": "Modern kitchen with Italian marble"
  },
  "model": "gpt-3.5-turbo"
}
```

#### Suggest Materials
```http
POST /ai/quotation/{id}/suggest
Content-Type: application/json

{
  "preferences": {
    "color_preference": "white",
    "finish_preference": "polished",
    "durability_priority": "high",
    "aesthetic_priority": "modern"
  },
  "model": "gpt-3.5-turbo"
}
```

#### Estimate Cost
```http
POST /ai/estimate-cost
Content-Type: application/json

{
  "area": 100,
  "material_type": "marble",
  "finish": "polished",
  "labor_rate": 25
}
```

---

### Export

#### Export Quotation as PDF
```http
GET /export/quotation/{id}/pdf
```
**Response:** PDF file

#### Export Quotation as Excel
```http
GET /export/quotation/{id}/excel
```
**Response:** Excel file (xlsx)

#### Export Quotation as Word
```http
GET /export/quotation/{id}/word
```
**Response:** Word document (docx)

---

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `500`: Server Error

---

## Rate Limiting
Currently no rate limiting. Will be added in production.

## Pagination
All list endpoints support pagination:
- `page`: Current page (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

## Sorting
Support for sorting to be added in future versions.

## Filtering
Advanced filtering to be added in future versions.

---

## Examples

### Create a complete quotation workflow

1. **Create a customer**
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "ABC Corp"
  }'
```

2. **Generate AI quotation**
```bash
curl -X POST http://localhost:5000/api/ai/quotation/generate \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "requirements": {
      "project_type": "Kitchen Countertop",
      "area": 100,
      "finish": "polished",
      "budget": 5000,
      "description": "Modern kitchen"
    }
  }'
```

3. **Export as PDF**
```bash
curl -X GET http://localhost:5000/api/export/quotation/1/pdf \
  -o quotation.pdf
```

---

## WebSocket Support (Planned)
- Real-time quotation updates
- Live material availability

## Future Enhancements
- Authentication & Authorization
- Advanced search and filtering
- Webhooks for external integrations
- GraphQL API
- Rate limiting
- API versioning
