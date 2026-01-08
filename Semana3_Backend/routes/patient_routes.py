from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.patient import Paciente
from models.base import db
from services.crypto_service import get_crypto_service
from datetime import datetime

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/v1/patients')


@patient_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    """Obtener todos los pacientes"""
    try:
        patients = Paciente.query.all()
        
        result = []
        for Paciente in patients:
            patient_data = {
                'id': Paciente.id,
                'first_name': Paciente.first_name,
                'last_name': Paciente.last_name,
                'date_of_birth': Paciente.date_of_birth.isoformat() if Paciente.date_of_birth else None,
                'gender': Paciente.gender,
                'blood_type': Paciente.blood_type,
                'phone': Paciente.phone,
                'email': Paciente.email,
                'address': Paciente.address,
                'emergency_contact': Paciente.emergency_contact,
                'created_at': Paciente.created_at.isoformat() if Paciente.created_at else None,
                'updated_at': Paciente.updated_at.isoformat() if Paciente.updated_at else None
            }
            
            # Descifrar campos sensibles
            if Paciente.allergies:
                try:
                    patient_data['allergies'] = get_crypto_service().decrypt_aes(Paciente.allergies)
                except:
                    patient_data['allergies'] = None
            else:
                patient_data['allergies'] = None
                
            if Paciente.medical_history:
                try:
                    patient_data['medical_history'] = get_crypto_service().decrypt_aes(Paciente.medical_history)
                except:
                    patient_data['medical_history'] = None
            else:
                patient_data['medical_history'] = None
            
            result.append(patient_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/', methods=['POST'])
@jwt_required()
def create_patient():
    """Crear un nuevo paciente"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['first_name', 'last_name', 'date_of_birth']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Cifrar campos sensibles
        encrypted_allergies = None
        if data.get('allergies'):
            encrypted_allergies = get_crypto_service().encrypt_aes(data['allergies'])
        
        encrypted_history = None
        if data.get('medical_history'):
            encrypted_history = get_crypto_service().encrypt_aes(data['medical_history'])
        
        # Crear paciente
        Paciente = Paciente(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.fromisoformat(data['date_of_birth'].replace('Z', '+00:00')),
            gender=data.get('gender'),
            blood_type=data.get('blood_type'),
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            allergies=encrypted_allergies,
            medical_history=encrypted_history,
            emergency_contact=data.get('emergency_contact')
        )
        
        db.session.add(Paciente)
        db.session.commit()
        
        # Preparar respuesta
        response_data = {
            'id': Paciente.id,
            'first_name': Paciente.first_name,
            'last_name': Paciente.last_name,
            'date_of_birth': Paciente.date_of_birth.isoformat(),
            'gender': Paciente.gender,
            'blood_type': Paciente.blood_type,
            'phone': Paciente.phone,
            'email': Paciente.email,
            'address': Paciente.address,
            'allergies': data.get('allergies'),
            'medical_history': data.get('medical_history'),
            'emergency_contact': Paciente.emergency_contact,
            'created_at': Paciente.created_at.isoformat()
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_patient(id):
    """Obtener un paciente por ID"""
    try:
        Paciente = Paciente.query.get(id)
        
        if not Paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        patient_data = {
            'id': Paciente.id,
            'first_name': Paciente.first_name,
            'last_name': Paciente.last_name,
            'date_of_birth': Paciente.date_of_birth.isoformat() if Paciente.date_of_birth else None,
            'gender': Paciente.gender,
            'blood_type': Paciente.blood_type,
            'phone': Paciente.phone,
            'email': Paciente.email,
            'address': Paciente.address,
            'emergency_contact': Paciente.emergency_contact,
            'created_at': Paciente.created_at.isoformat() if Paciente.created_at else None,
            'updated_at': Paciente.updated_at.isoformat() if Paciente.updated_at else None
        }
        
        # Descifrar campos sensibles
        if Paciente.allergies:
            try:
                patient_data['allergies'] = get_crypto_service().decrypt_aes(Paciente.allergies)
            except:
                patient_data['allergies'] = None
        else:
            patient_data['allergies'] = None
            
        if Paciente.medical_history:
            try:
                patient_data['medical_history'] = get_crypto_service().decrypt_aes(Paciente.medical_history)
            except:
                patient_data['medical_history'] = None
        else:
            patient_data['medical_history'] = None
        
        return jsonify(patient_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):
    """Actualizar un paciente"""
    try:
        Paciente = Paciente.query.get(id)
        
        if not Paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar campos básicos
        if 'first_name' in data:
            Paciente.first_name = data['first_name']
        if 'last_name' in data:
            Paciente.last_name = data['last_name']
        if 'date_of_birth' in data:
            Paciente.date_of_birth = datetime.fromisoformat(data['date_of_birth'].replace('Z', '+00:00'))
        if 'gender' in data:
            Paciente.gender = data['gender']
        if 'blood_type' in data:
            Paciente.blood_type = data['blood_type']
        if 'phone' in data:
            Paciente.phone = data['phone']
        if 'email' in data:
            Paciente.email = data['email']
        if 'address' in data:
            Paciente.address = data['address']
        if 'emergency_contact' in data:
            Paciente.emergency_contact = data['emergency_contact']
        
        # Actualizar campos cifrados
        if 'allergies' in data:
            if data['allergies']:
                Paciente.allergies = get_crypto_service().encrypt_aes(data['allergies'])
            else:
                Paciente.allergies = None
                
        if 'medical_history' in data:
            if data['medical_history']:
                Paciente.medical_history = get_crypto_service().encrypt_aes(data['medical_history'])
            else:
                Paciente.medical_history = None
        
        Paciente.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Preparar respuesta
        response_data = {
            'id': Paciente.id,
            'first_name': Paciente.first_name,
            'last_name': Paciente.last_name,
            'date_of_birth': Paciente.date_of_birth.isoformat() if Paciente.date_of_birth else None,
            'gender': Paciente.gender,
            'blood_type': Paciente.blood_type,
            'phone': Paciente.phone,
            'email': Paciente.email,
            'address': Paciente.address,
            'emergency_contact': Paciente.emergency_contact,
            'updated_at': Paciente.updated_at.isoformat()
        }
        
        # Descifrar para respuesta
        if Paciente.allergies:
            try:
                response_data['allergies'] = get_crypto_service().decrypt_aes(Paciente.allergies)
            except:
                response_data['allergies'] = None
        else:
            response_data['allergies'] = None
            
        if Paciente.medical_history:
            try:
                response_data['medical_history'] = get_crypto_service().decrypt_aes(Paciente.medical_history)
            except:
                response_data['medical_history'] = None
        else:
            response_data['medical_history'] = None
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    """Eliminar un paciente"""
    try:
        Paciente = Paciente.query.get(id)
        
        if not Paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        db.session.delete(Paciente)
        db.session.commit()
        
        return jsonify({'message': 'Paciente eliminado correctamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

