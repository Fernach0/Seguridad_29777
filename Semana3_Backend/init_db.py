"""
Script de Inicialización de Base de Datos
Crea las tablas y un usuario administrador por defecto
"""
from app import create_app, db
from models.user import Usuario
from services.crypto_service import get_crypto_service
import os


def init_database():
    """Inicializar base de datos"""
    app = create_app()
    
    with app.app_context():
        print("🔧 Creando tablas de base de datos...")
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        # Verificar si ya existe un admin
        admin_exists = Usuario.query.filter_by(username='admin').first()
        
        if not admin_exists:
            print("\n👤 Creando usuario administrador por defecto...")
            
            # Crear admin
            password = 'Admin123!'  # Cambiar en producción
            password_hash = get_crypto_service().hash_password(password)
            
            admin = Usuario(
                username='admin',
                password_hash=password_hash,
                salt='',  # bcrypt incluye el salt en el hash
                email='admin@espe.edu.ec',
                nombre='Administrador',
                apellido='Sistema',
                cedula='0000000000',
                rol='admin',
                activo=True
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Usuario administrador creado:")
            print(f"   Username: admin")
            print(f"   Password: {password}")
            print(f"   ⚠️  IMPORTANTE: Cambiar la contraseña después del primer login")
        else:
            print("\n✅ Usuario administrador ya existe")
        
        print("\n🎉 Base de datos inicializada correctamente")
        print(f"\n📝 Configuración:")
        print(f"   - Base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"   - Modo: {app.config['ENV']}")
        print(f"\n🚀 Puedes iniciar la aplicación con: python app.py")


if __name__ == '__main__':
    init_database()
