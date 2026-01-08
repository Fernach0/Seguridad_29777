"""
Rutas de Autenticación
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    try:
        data = request.get_json()
        
        # Validar datos
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'error': 'Username y password son requeridos'
            }), 400
        
        # Autenticar
        token, usuario = AuthService.login(data['username'], data['password'])
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Credenciales inválidas'
            }), 401
        
        return jsonify({
            'success': True,
            'data': {
                'token': token,
                'user': usuario.to_dict()
            },
            'message': 'Login exitoso'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtener usuario actual"""
    try:
        user_id = get_jwt_identity()
        usuario = AuthService.get_user_by_id(user_id)
        
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': usuario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Cerrar sesión"""
    try:
        user_id = get_jwt_identity()
        
        # Registrar logout en auditoría
        AuthService.log_audit(
            usuario_id=user_id,
            accion='LOGOUT',
            tabla_afectada='usuarios'
        )
        
        return jsonify({
            'success': True,
            'message': 'Sesión cerrada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor'
        }), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar nuevo usuario (solo para testing/desarrollo)"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['username', 'password', 'rol', 'nombre', 
                          'apellido', 'email', 'cedula']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }), 400
        
        # Registrar usuario
        usuario = AuthService.register_user(
            username=data['username'],
            password=data['password'],
            rol=data['rol'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            cedula=data['cedula']
        )
        
        return jsonify({
            'success': True,
            'data': usuario.to_dict(),
            'message': 'Usuario creado exitosamente'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500
