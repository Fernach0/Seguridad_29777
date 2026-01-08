"""
Utilidades de Validación
"""
import re
from datetime import datetime


def validate_email(email):
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_cedula_ecuador(cedula):
    """
    Validar cédula ecuatoriana (10 dígitos con dígito verificador)
    Algoritmo: módulo 10
    """
    if not cedula or len(cedula) != 10:
        return False
    
    try:
        # Verificar que sean números
        int(cedula)
        
        # Coeficientes para multiplicar
        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        
        # Los primeros 9 dígitos
        digitos = [int(d) for d in cedula[:9]]
        
        # Multiplicar y sumar
        suma = 0
        for i, digito in enumerate(digitos):
            producto = digito * coeficientes[i]
            if producto >= 10:
                producto -= 9
            suma += producto
        
        # Calcular dígito verificador
        modulo = suma % 10
        digito_verificador = 0 if modulo == 0 else 10 - modulo
        
        # Comparar con el último dígito
        return digito_verificador == int(cedula[9])
        
    except (ValueError, IndexError):
        return False


def validate_phone(phone):
    """Validar formato de teléfono (Ecuador: 10 dígitos)"""
    if not phone:
        return True  # Campo opcional
    
    # Remover espacios y guiones
    phone_clean = phone.replace(' ', '').replace('-', '')
    
    # Validar longitud y que sean números
    if len(phone_clean) != 10:
        return False
    
    try:
        int(phone_clean)
        return True
    except ValueError:
        return False


def validate_date(date_string, format='%Y-%m-%d'):
    """Validar formato de fecha"""
    try:
        datetime.strptime(date_string, format)
        return True
    except (ValueError, TypeError):
        return False


def validate_password_strength(password):
    """
    Validar fortaleza de contraseña
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    if not password or len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una minúscula"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, "Contraseña válida"


def validate_username(username):
    """
    Validar nombre de usuario
    - Solo letras, números y guiones bajos
    - Entre 3 y 30 caracteres
    """
    if not username or len(username) < 3 or len(username) > 30:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None


def sanitize_input(text):
    """Sanitizar entrada de texto (prevenir XSS básico)"""
    if not text:
        return text
    
    # Remover caracteres peligrosos
    dangerous_chars = ['<', '>', '"', "'", '&']
    sanitized = text
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def validate_grupo_sanguineo(grupo):
    """Validar grupo sanguíneo"""
    grupos_validos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return grupo in grupos_validos if grupo else True


def validate_genero(genero):
    """Validar género"""
    generos_validos = ['M', 'F', 'Otro']
    return genero in generos_validos if genero else True


def validate_rol(rol):
    """Validar rol de usuario"""
    roles_validos = ['admin', 'doctor', 'paciente']
    return rol in roles_validos
