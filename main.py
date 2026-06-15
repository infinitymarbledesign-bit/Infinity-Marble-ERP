"""Updated main.py with pricelist routes and assets configuration"""
import os
import sys
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()

@app.route('/')
def index():
    """Health check endpoint"""
    return {
        'status': 'ok',
        'message': 'Infinity Marble ERP API',
        'version': '1.0.0',
        'endpoints': {
            'api': '/api',
            'customers': '/api/customers',
            'materials': '/api/materials',
            'quotations': '/api/quotations',
            'invoices': '/api/invoices',
            'price_list': '/api/pricelist',
            'ai': '/api/ai',
            'export': '/api/export'
        }
    }

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}

@app.route('/docs')
def docs():
    """Documentation endpoint"""
    return {
        'message': 'See API_DOCUMENTATION.md for full API docs',
        'file': 'API_DOCUMENTATION.md'
    }

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    
    print(f"🚀 Starting Infinity Marble ERP API")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print(f"\n📚 Available endpoints:")
    print(f"   - Customers: http://{host}:{port}/api/customers")
    print(f"   - Materials: http://{host}:{port}/api/materials")
    print(f"   - Quotations: http://{host}:{port}/api/quotations")
    print(f"   - Invoices: http://{host}:{port}/api/invoices")
    print(f"   - Price List: http://{host}:{port}/api/pricelist")
    print(f"   - AI: http://{host}:{port}/api/ai")
    print(f"   - Export: http://{host}:{port}/api/export")
    
    app.run(host=host, port=port, debug=debug)
