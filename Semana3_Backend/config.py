"""
Configuración de la aplicación ESPE MedSafe
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-por-defecto-cambiar')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/espe_medsafe'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # Log SQL queries in debug mode
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-cambiar')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1800))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Cryptography
    AES_MASTER_KEY = os.getenv('AES_MASTER_KEY', '')
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']  # React dev servers
    
    # Application
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Pagination
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # Bcrypt
    BCRYPT_LOG_ROUNDS = 12  # Factor de trabajo para bcrypt


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # En producción, asegurarse de que las claves estén configuradas
    @classmethod
    def validate(cls):
        """Validar que las variables críticas estén configuradas"""
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY debe estar configurada en producción")
        if not os.getenv('JWT_SECRET_KEY'):
            raise ValueError("JWT_SECRET_KEY debe estar configurada en producción")
        if not os.getenv('AES_MASTER_KEY'):
            raise ValueError("AES_MASTER_KEY debe estar configurada en producción")


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=300)


# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtener configuración según el entorno"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
