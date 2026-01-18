from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.patient import Paciente
from models.base import db
from services.crypto_service import get_crypto_service
from utils.validators import validate_cedula_ecuador
from datetime import datetime

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/v1/patients')


@patient_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    """Obtener todos los pacientes"""
    try:
        patients = Paciente.query.all()
        
        result = []
        for paciente in patients:
            patient_data = {
                'id': paciente.id,
                'cedula': paciente.cedula,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
                'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                'genero': paciente.genero,
                'grupo_sanguineo': paciente.grupo_sanguineo,
                'telefono': paciente.telefono,
                'email': paciente.email,
                'direccion': paciente.direccion,
                'created_at': paciente.created_at.isoformat() if paciente.created_at else None,
                'updated_at': paciente.updated_at.isoformat() if paciente.updated_at else None
            }
            
            # Descifrar campos sensibles
            if paciente.alergias_encrypted and paciente.alergias_iv:
                try:
                    patient_data['alergias'] = get_crypto_service().decrypt_aes(
                        paciente.alergias_encrypted, 
                        paciente.alergias_iv
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando alergias: {e}")
                    patient_data['alergias'] = None
            else:
                patient_data['alergias'] = None
                
            if paciente.antecedentes_encrypted and paciente.antecedentes_iv:
                try:
                    patient_data['antecedentes'] = get_crypto_service().decrypt_aes(
                        paciente.antecedentes_encrypted,
                        paciente.antecedentes_iv
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando antecedentes: {e}")
                    patient_data['antecedentes'] = None
            else:
                patient_data['antecedentes'] = None
            
            result.append(patient_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo pacientes: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/', methods=['POST'])
@jwt_required()
def create_patient():
    """Crear un nuevo paciente"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre', 'apellido', 'cedula', 'fecha_nacimiento']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Validar cédula ecuatoriana
        if not validate_cedula_ecuador(data['cedula']):
            return jsonify({
                'success': False,
                'error': 'Cédula ecuatoriana inválida. Debe ser una cédula válida de 10 dígitos.'
            }), 400
        
        # Verificar si la cédula ya existe
        existing_patient = Paciente.query.filter_by(cedula=data['cedula']).first()
        if existing_patient:
            return jsonify({
                'success': False,
                'error': f'La cédula {data["cedula"]} ya está registrada'
            }), 400
        
        # Cifrar campos sensibles
        encrypted_alergias = None
        alergias_iv = None
        if data.get('alergias'):
            encrypted_alergias, alergias_iv = get_crypto_service().encrypt_aes(data['alergias'])
        
        encrypted_antecedentes = None
        antecedentes_iv = None
        if data.get('antecedentes'):
            encrypted_antecedentes, antecedentes_iv = get_crypto_service().encrypt_aes(data['antecedentes'])
        
        # Crear paciente
        paciente = Paciente(
            cedula=data['cedula'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            fecha_nacimiento=datetime.fromisoformat(data['fecha_nacimiento'].replace('Z', '+00:00')).date(),
            genero=data.get('genero'),
            grupo_sanguineo=data.get('tipo_sangre'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            alergias_encrypted=encrypted_alergias,
            alergias_iv=alergias_iv,
            antecedentes_encrypted=encrypted_antecedentes,
            antecedentes_iv=antecedentes_iv
        )
        
        db.session.add(paciente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': paciente.to_dict(include_encrypted=False),
            'message': 'Paciente creado exitosamente'
        }), 201
        
    except ValueError as ve:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creando paciente: {str(e)}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500


@patient_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_patient(id):
    """Obtener un paciente por ID"""
    try:
        paciente = Paciente.query.get(id)
        
        if not paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        patient_data = {
            'id': paciente.id,
            'cedula': paciente.cedula,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
            'genero': paciente.genero,
            'grupo_sanguineo': paciente.grupo_sanguineo,
            'telefono': paciente.telefono,
            'email': paciente.email,
            'direccion': paciente.direccion,
            'created_at': paciente.created_at.isoformat() if paciente.created_at else None,
            'updated_at': paciente.updated_at.isoformat() if paciente.updated_at else None
        }
        
        # Descifrar campos sensibles
        if paciente.alergias_encrypted and paciente.alergias_iv:
            try:
                patient_data['alergias'] = get_crypto_service().decrypt_aes(
                    paciente.alergias_encrypted,
                    paciente.alergias_iv
                )
            except Exception as e:
                print(f"⚠️  Error descifrando alergias: {e}")
                patient_data['alergias'] = None
        else:
            patient_data['alergias'] = None
            
        if paciente.antecedentes_encrypted and paciente.antecedentes_iv:
            try:
                patient_data['antecedentes'] = get_crypto_service().decrypt_aes(
                    paciente.antecedentes_encrypted,
                    paciente.antecedentes_iv
                )
            except Exception as e:
                print(f"⚠️  Error descifrando antecedentes: {e}")
                patient_data['antecedentes'] = None
        else:
            patient_data['antecedentes'] = None
        
        return jsonify(patient_data), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo paciente {id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):
    """Actualizar un paciente"""
    try:
        paciente = Paciente.query.get(id)
        
        if not paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar campos básicos
        if 'nombre' in data:
            paciente.nombre = data['nombre']
        if 'apellido' in data:
            paciente.apellido = data['apellido']
        if 'fecha_nacimiento' in data:
            paciente.fecha_nacimiento = datetime.fromisoformat(data['fecha_nacimiento'].replace('Z', '+00:00')).date()
        if 'genero' in data:
            paciente.genero = data['genero']
        if 'grupo_sanguineo' in data or 'tipo_sangre' in data:
            paciente.grupo_sanguineo = data.get('grupo_sanguineo') or data.get('tipo_sangre')
        if 'telefono' in data:
            paciente.telefono = data['telefono']
        if 'email' in data:
            paciente.email = data['email']
        if 'direccion' in data:
            paciente.direccion = data['direccion']
        
        # Actualizar campos cifrados
        if 'alergias' in data:
            if data['alergias']:
                encrypted_alergias, alergias_iv = get_crypto_service().encrypt_aes(data['alergias'])
                paciente.alergias_encrypted = encrypted_alergias
                paciente.alergias_iv = alergias_iv
            else:
                paciente.alergias_encrypted = None
                paciente.alergias_iv = None
                
        if 'antecedentes' in data:
            if data['antecedentes']:
                encrypted_antecedentes, antecedentes_iv = get_crypto_service().encrypt_aes(data['antecedentes'])
                paciente.antecedentes_encrypted = encrypted_antecedentes
                paciente.antecedentes_iv = antecedentes_iv
            else:
                paciente.antecedentes_encrypted = None
                paciente.antecedentes_iv = None
        
        paciente.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Preparar respuesta
        response_data = {
            'id': paciente.id,
            'cedula': paciente.cedula,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
            'genero': paciente.genero,
            'grupo_sanguineo': paciente.grupo_sanguineo,
            'telefono': paciente.telefono,
            'email': paciente.email,
            'direccion': paciente.direccion,
            'updated_at': paciente.updated_at.isoformat()
        }
        
        # Descifrar para respuesta
        if paciente.alergias_encrypted and paciente.alergias_iv:
            try:
                response_data['alergias'] = get_crypto_service().decrypt_aes(
                    paciente.alergias_encrypted,
                    paciente.alergias_iv
                )
            except Exception as e:
                print(f"⚠️  Error descifrando alergias: {e}")
                response_data['alergias'] = None
        else:
            response_data['alergias'] = None
            
        if paciente.antecedentes_encrypted and paciente.antecedentes_iv:
            try:
                response_data['antecedentes'] = get_crypto_service().decrypt_aes(
                    paciente.antecedentes_encrypted,
                    paciente.antecedentes_iv
                )
            except Exception as e:
                print(f"⚠️  Error descifrando antecedentes: {e}")
                response_data['antecedentes'] = None
        else:
            response_data['antecedentes'] = None
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error actualizando paciente {id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    """Eliminar un paciente"""
    try:
        paciente = Paciente.query.get(id)
        
        if not paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        db.session.delete(paciente)
        db.session.commit()
        
        return jsonify({'message': 'Paciente eliminado correctamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error eliminando paciente {id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

