"""
Funciones de Ayuda
"""
from datetime import datetime, date
import base64


def calculate_age(birth_date):
    """Calcular edad a partir de fecha de nacimiento"""
    if not birth_date:
        return None
    
    today = date.today()
    age = today.year - birth_date.year
    
    # Ajustar si aún no cumplió años este año
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age


def format_date(date_obj, format='%Y-%m-%d'):
    """Formatear objeto fecha a string"""
    if not date_obj:
        return None
    
    if isinstance(date_obj, str):
        return date_obj
    
    return date_obj.strftime(format)


def format_datetime(datetime_obj, format='%Y-%m-%d %H:%M:%S'):
    """Formatear objeto datetime a string"""
    if not datetime_obj:
        return None
    
    if isinstance(datetime_obj, str):
        return datetime_obj
    
    return datetime_obj.strftime(format)


def encode_base64(data):
    """Codificar datos en base64"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')


def decode_base64(data):
    """Decodificar datos de base64"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64decode(data).decode('utf-8')


def mask_sensitive_data(data, visible_chars=4):
    """Enmascarar datos sensibles (mostrar solo últimos caracteres)"""
    if not data or len(data) <= visible_chars:
        return '*' * len(data) if data else ''
    
    return '*' * (len(data) - visible_chars) + data[-visible_chars:]


def parse_date(date_string, format='%Y-%m-%d'):
    """Convertir string a objeto date"""
    try:
        return datetime.strptime(date_string, format).date()
    except (ValueError, TypeError):
        return None


def parse_datetime(datetime_string, format='%Y-%m-%d %H:%M:%S'):
    """Convertir string a objeto datetime"""
    try:
        return datetime.strptime(datetime_string, format)
    except (ValueError, TypeError):
        return None


def paginate_query(query, page=1, per_page=10):
    """
    Paginar query de SQLAlchemy
    Retorna diccionario con items y metadata de paginación
    """
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': pagination.items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }


def get_client_ip(request):
    """Obtener IP del cliente desde request"""
    # Verificar headers de proxy
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr


def success_response(data=None, message=None, status=200):
    """Formatear respuesta exitosa"""
    response = {'success': True}
    
    if data is not None:
        response['data'] = data
    
    if message:
        response['message'] = message
    
    return response, status


def error_response(error, status=400, details=None):
    """Formatear respuesta de error"""
    response = {
        'success': False,
        'error': error
    }
    
    if details:
        response['details'] = details
    
    return response, status


def format_nombre_completo(nombre, apellido):
    """Formatear nombre completo"""
    return f"{nombre} {apellido}".strip()


def generate_file_name(prefix, extension):
    """Generar nombre único para archivo"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"


def truncate_text(text, max_length=100, suffix='...'):
    """Truncar texto largo"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
