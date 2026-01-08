"""
Rutas de Auditoría (Admin)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime
from models.base import db
from models.audit_log import AuditLog

audit_bp = Blueprint('audit', __name__)


def require_admin():
    """Verificar que el usuario sea administrador"""
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({
            'success': False,
            'error': 'Acceso denegado. Se requiere rol de administrador.'
        }), 403
    return None


@audit_bp.route('', methods=['GET'])
@jwt_required()
def get_audit_logs():
    """Obtener logs de auditoría - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        # Parámetros de filtro
        accion = request.args.get('accion')
        usuario_id = request.args.get('usuario_id', type=int)
        tabla = request.args.get('tabla')
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        # Construir query
        query = AuditLog.query
        
        if accion:
            query = query.filter_by(accion=accion)
        
        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        
        if tabla:
            query = query.filter_by(tabla_afectada=tabla)
        
        if fecha_desde:
            fecha = datetime.strptime(fecha_desde, '%Y-%m-%d')
            query = query.filter(AuditLog.timestamp >= fecha)
        
        if fecha_hasta:
            fecha = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            query = query.filter(AuditLog.timestamp <= fecha)
        
        # Ordenar por más reciente
        query = query.order_by(AuditLog.timestamp.desc())
        
        # Paginar
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'logs': [log.to_dict() for log in pagination.items],
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


@audit_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_audit_logs(user_id):
    """Obtener logs de un usuario específico - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        query = AuditLog.query.filter_by(usuario_id=user_id).order_by(
            AuditLog.timestamp.desc()
        )
        
        pagination = query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'usuario_id': user_id,
                'logs': [log.to_dict() for log in pagination.items],
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


@audit_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_audit_stats():
    """Obtener estadísticas de auditoría - Solo admin"""
    error_response = require_admin()
    if error_response:
        return error_response
    
    try:
        # Contar por acción
        acciones = db.session.query(
            AuditLog.accion,
            db.func.count(AuditLog.id).label('count')
        ).group_by(AuditLog.accion).all()
        
        # Contar por tabla
        tablas = db.session.query(
            AuditLog.tabla_afectada,
            db.func.count(AuditLog.id).label('count')
        ).group_by(AuditLog.tabla_afectada).all()
        
        # Total de logs
        total = AuditLog.query.count()
        
        # Logs de hoy
        today = datetime.now().date()
        logs_hoy = AuditLog.query.filter(
            db.func.date(AuditLog.timestamp) == today
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_logs': total,
                'logs_hoy': logs_hoy,
                'por_accion': {accion: count for accion, count in acciones},
                'por_tabla': {tabla: count for tabla, count in tablas}
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500
