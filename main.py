"""Main entry point for Infinity Marble ERP application"""
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
        'version': '1.0.0'
    }

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    
    print(f"🚀 Starting Infinity Marble ERP API")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    
    app.run(host=host, port=port, debug=debug)
