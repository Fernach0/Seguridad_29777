"""
Aplicación principal - ESPE MedSafe Backend
"""
import os
import base64
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from models.base import db
from services.crypto_service import init_crypto_service

# Import routes
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.patient_routes import patient_bp
from routes.medical_record_routes import medical_record_bp
from routes.audit_routes import audit_bp
from routes.crypto_routes import crypto_bp


def create_app(config_name=None):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        app: Aplicación Flask configurada
    """
    app = Flask(__name__)
    
    # Configurar Flask para no redirigir barras finales
    app.url_map.strict_slashes = False
    
    # Cargar configuración
    if config_name:
        app.config.from_object(config_name)
    else:
        config_class = get_config()
        app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    jwt = JWTManager(app)
    
    # Inicializar servicio criptográfico
    with app.app_context():
        aes_key = app.config.get('AES_MASTER_KEY')
        if not aes_key:
            # Generar clave temporal para desarrollo
            print("⚠️  WARNING: Generando clave AES temporal. Configura AES_MASTER_KEY en producción.")
            aes_key = base64.b64encode(os.urandom(32)).decode()
        
        init_crypto_service(aes_key)
    
    # Registrar blueprints (rutas)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(patient_bp, url_prefix='/api/v1/patients')
    app.register_blueprint(medical_record_bp, url_prefix='/api/v1/medical-records')
    app.register_blueprint(audit_bp, url_prefix='/api/v1/audit-logs')
    app.register_blueprint(crypto_bp, url_prefix='/api/v1/crypto')
    
    # Manejadores de errores JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print("⚠️  JWT Error: Token expirado")
        return jsonify({
            'success': False,
            'error': 'Token expirado',
            'message': 'El token ha expirado. Por favor, inicie sesión nuevamente.'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"⚠️  JWT Error: Token inválido - {error}")
        return jsonify({
            'success': False,
            'error': 'Token inválido',
            'message': 'El token proporcionado no es válido.'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"⚠️  JWT Error: Token no proporcionado - {error}")
        return jsonify({
            'success': False,
            'error': 'Token no proporcionado',
            'message': 'Se requiere autenticación para acceder a este recurso.'
        }), 401
    
    # Ruta de prueba
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'ESPE MedSafe API v1.0',
            'status': 'running'
        })
    
    @app.route('/health')
    def health():
        """Endpoint de salud para monitoreo"""
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected' if db.engine else 'disconnected'
        })
    
    # Manejo global de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint no encontrado'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    
    return app


# Crear aplicación
app = create_app()


if __name__ == '__main__':
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
        print("✅ Tablas de base de datos creadas")
    
    # Ejecutar aplicación
    print(f"🚀 ESPE MedSafe Backend iniciando en http://{app.config['HOST']}:{app.config['PORT']}")
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
