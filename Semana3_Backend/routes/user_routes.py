"""
Rutas de Usuarios (Admin)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models.base import db
from models.user import Usuario
from services.auth_service import AuthService

user_bp = Blueprint('users', __name__)


def require_admin():
    """Decorador para verificar que el usuario sea admin"""
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({
            'success': False,
            'error': 'Acceso denegado. Se requiere rol de administrador.'
        }), 403
    return None


@user_bp.route('', methods=['POST'])
@jwt_required()
def create_user():
    """Crear usuario (doctor) - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
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
        
        # Crear usuario
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


@user_bp.route('', methods=['GET'])
@jwt_required()
def list_users():
    """Listar usuarios - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        # Obtener parámetros de query
        rol = request.args.get('rol')
        activo = request.args.get('activo')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # Construir query
        query = Usuario.query
        
        if rol:
            query = query.filter_by(rol=rol)
        
        if activo is not None:
            activo_bool = activo.lower() == 'true'
            query = query.filter_by(activo=activo_bool)
        
        # Paginación
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'users': [user.to_dict() for user in pagination.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': pagination.total,
                    'pages': pagination.pages
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Obtener usuario por ID - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        usuario = Usuario.query.get(user_id)
        
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
            'error': 'Error en el servidor'
        }), 500


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Actualizar usuario - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        data = request.get_json()
        
        usuario = AuthService.update_user(user_id, **data)
        
        return jsonify({
            'success': True,
            'data': usuario.to_dict(),
            'message': 'Usuario actualizado exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Desactivar usuario - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        usuario = AuthService.deactivate_user(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Usuario desactivado exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor'
        }), 500
