import os
import logging
from flask import Flask
from models.database import db

# Configure logging for production
logging.basicConfig(level=logging.INFO)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Disable debug mode for production
app.config['DEBUG'] = False

# Import routes after app creation to avoid circular imports
try:
    from routes.main_routes import main_bp
    from routes.api_routes import api_bp
    from routes.dashboard_routes import dashboard_bp
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
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
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return {
        'status': 'healthy', 
        'service': 'sustainability-analytics',
        'database': db_status
    }, 200

# Create database tables
with app.app_context():
    try:
        db.create_all()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Database initialization error: {str(e)}")

# Vercel serverless function handler
def handler(environ, start_response):
    """WSGI handler for Vercel serverless functions"""
    return app(environ, start_response)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
