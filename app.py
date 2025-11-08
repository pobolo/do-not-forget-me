from flask import Flask, jsonify
from flask_cors import CORS
import logging
from routes.individuals import individuals_bp
from services.wealth_service import wealth_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(individuals_bp)
    
    # Health check route
    @app.route('/health')
    def health_check():
        try:
            redis_info = wealth_service.get_redis_info()
            return jsonify({
                'status': 'healthy',
                'redis': 'connected',
                'redis_info': redis_info
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'redis': 'disconnected',
                'error': str(e)
            }), 500
    
    # Statistics route
    @app.route('/stats')
    def get_stats():
        try:
            wealth_stats = wealth_service.get_wealth_statistics()
            redis_info = wealth_service.get_redis_info()
            
            return jsonify({
                'success': True,
                'wealth_statistics': wealth_stats,
                'redis_info': redis_info
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("Starting Wealth Tracker API...")
    print("Available routes:")
    print("  GET  /health - Health check")
    print("  GET  /stats - System statistics")
    print("  GET  /individuals - List all individuals")
    print("  POST /individuals - Create new individual")
    print("  GET  /individuals/<id> - Get individual by ID")
    print("  PUT  /individuals/<id> - Update individual")
    print("  DELETE /individuals/<id> - Delete individual")
    print("  GET  /individuals/ranking - Wealth ranking")
    print("  GET  /individuals/industry/<industry> - Filter by industry")
    print("  GET  /individuals/search?q=query - Search individuals")
    
    app.run(debug=True, host='0.0.0.0', port=5000)