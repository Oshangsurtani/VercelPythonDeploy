import os
import logging
from flask import Flask

# Configure logging for production
logging.basicConfig(level=logging.INFO)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Disable debug mode for production
app.config['DEBUG'] = False

# Import routes after app creation to avoid circular imports
try:
    from routes.main_routes import main_bp
    from routes.api_routes import api_bp
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
except ImportError as e:
    logging.error(f"Error importing routes: {str(e)}")

@app.errorhandler(404)
def not_found_error(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Internal server error: {str(error)}")
    return {'error': 'Internal server error'}, 500

@app.route('/health')
def health_check():
    """Health check endpoint for Vercel"""
    return {'status': 'healthy', 'service': 'sustainability-analytics'}, 200

# Vercel serverless function handler
def handler(environ, start_response):
    """WSGI handler for Vercel serverless functions"""
    return app(environ, start_response)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
