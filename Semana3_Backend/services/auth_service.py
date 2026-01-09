"""
Servicio de autenticación y autorización
Gestiona registro, login, actualización de usuarios y auditoría
"""
import json
from datetime import datetime
from flask import request
from flask_jwt_extended import create_access_token
from models.base import db
from models.user import Usuario
from models.audit_log import AuditLog
from services.crypto_service import get_crypto_service
from utils.validators import validate_cedula_ecuador, validate_email


class AuthService:
    """Servicio para gestionar autenticación y autorización de usuarios"""
    
    @staticmethod
    def register_user(username, password, email, rol='medico', nombre='', apellido='', cedula=''):
        """
        Registrar un nuevo usuario en el sistema
        
        Args:
            username: Nombre de usuario único
            password: Contraseña en texto plano (se hasheará)
            email: Email del usuario
            rol: Rol del usuario (admin, doctor)
            nombre: Nombre del usuario
            apellido: Apellido del usuario
            cedula: Cédula ecuatoriana (10 dígitos)
            
        Returns:
            Usuario creado o lanza ValueError si hay error de validación
        """
        try:
            # Validar cédula ecuatoriana
            if cedula and not validate_cedula_ecuador(cedula):
                raise ValueError('Cédula ecuatoriana inválida. Debe ser una cédula válida de 10 dígitos.')
            
            # Validar email
            if not validate_email(email):
                raise ValueError('Formato de email inválido')
            
            # Verificar si el usuario ya existe
            existing_user = Usuario.query.filter_by(username=username).first()
            if existing_user:
                raise ValueError(f'El usuario {username} ya existe')
            
            # Verificar si la cédula ya existe
            if cedula:
                existing_cedula = Usuario.query.filter_by(cedula=cedula).first()
                if existing_cedula:
                    raise ValueError(f'La cédula {cedula} ya está registrada')
            
            # Verificar si el email ya existe
            existing_email = Usuario.query.filter_by(email=email).first()
            if existing_email:
                raise ValueError(f'El email {email} ya está registrado')
            
            # Hashear la contraseña usando el crypto_service
            password_hash = get_crypto_service().hash_password(password)
            
            # Crear nuevo usuario
            nuevo_usuario = Usuario(
                username=username,
                password_hash=password_hash,
                email=email,
                rol=rol,
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                activo=True
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            # Registrar auditoría
            AuthService.log_audit(
                user_id=nuevo_usuario.id,
                action='REGISTER',
                description=f'Usuario {username} registrado exitosamente'
            )
            
            return nuevo_usuario
            
        except ValueError as ve:
            db.session.rollback()
            raise ve
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar usuario: {str(e)}")
            raise ValueError(f'Error al registrar usuario: {str(e)}')
    
    @staticmethod
    def login(username, password):
        """
        Autenticar usuario y generar token JWT
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            dict con token y datos del usuario, o None si falla
        """
        try:
            # Buscar usuario
            usuario = Usuario.query.filter_by(username=username).first()
            
            if not usuario:
                return None
            
            # Verificar contraseña usando crypto_service
            if not get_crypto_service().verify_password(password, usuario.password_hash):
                # Registrar intento fallido
                AuthService.log_audit(
                    user_id=usuario.id,
                    action='LOGIN_FAILED',
                    description=f'Intento de login fallido para usuario {username}'
                )
                return None
            
            # Crear token JWT con claims adicionales
            access_token = create_access_token(
                identity=str(usuario.id),  # El subject debe ser un string
                additional_claims={
                    'username': usuario.username,
                    'rol': usuario.rol
                }
            )
            
            # Registrar login exitoso
            AuthService.log_audit(
                user_id=usuario.id,
                action='LOGIN',
                description=f'Usuario {username} inició sesión exitosamente'
            )
            
            # Retornar token y usuario
            return access_token, usuario
            
        except Exception as e:
            print(f"Error en login: {str(e)}")
            return None, None
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Obtener usuario por ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Usuario o None si no existe
        """
        try:
            return Usuario.query.get(user_id)
        except Exception as e:
            print(f"Error al obtener usuario: {str(e)}")
            return None
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Actualizar datos de un usuario
        
        Args:
            user_id: ID del usuario a actualizar
            **kwargs: Campos a actualizar (username, email, password, rol)
            
        Returns:
            Usuario actualizado o None si falla
        """
        try:
            usuario = Usuario.query.get(user_id)
            if not usuario:
                return None
            
            # Actualizar campos
            if 'username' in kwargs:
                usuario.username = kwargs['username']
            
            if 'email' in kwargs:
                usuario.email = kwargs['email']
            
            if 'password' in kwargs:
                # Hashear nueva contraseña
                usuario.password_hash = get_crypto_service().hash_password(kwargs['password'])
            
            if 'rol' in kwargs:
                usuario.rol = kwargs['rol']
            
            db.session.commit()
            
            # Registrar auditoría
            AuthService.log_audit(
                user_id=user_id,
                action='UPDATE_USER',
                description=f'Usuario {usuario.username} actualizado'
            )
            
            return usuario
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar usuario: {str(e)}")
            return None
    
    @staticmethod
    def log_audit(user_id, action, description, additional_data=None):
        """
        Registrar acción en el log de auditoría
        
        Args:
            user_id: ID del usuario que realiza la acción
            action: Tipo de acción (LOGIN, REGISTER, etc.)
            description: Descripción de la acción
            additional_data: Datos adicionales en formato dict
        """
        try:
            # Obtener IP del request si está disponible
            ip_address = None
            if request:
                ip_address = request.remote_addr
            
            # Convertir additional_data a JSON si se proporciona
            datos_json = None
            if additional_data:
                datos_json = json.dumps(additional_data)
            
            # Crear registro de auditoría
            audit_log = AuditLog(
                usuario_id=user_id,
                accion=action,
                tabla_afectada=description,
                ip_address=ip_address,
                datos_nuevos=datos_json
            )
            
            db.session.add(audit_log)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar auditoría: {str(e)}")
