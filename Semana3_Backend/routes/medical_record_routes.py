from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.medical_record import HistoriaClinica
from models.patient import Paciente
from models.base import db
from services.crypto_service import get_crypto_service
from datetime import datetime

medical_record_bp = Blueprint('medical_record_bp', __name__, url_prefix='/api/v1/medical-records')


@medical_record_bp.route('/Paciente/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_records(patient_id):
    """Obtener todos los registros médicos de un paciente"""
    try:
        # Verificar que el paciente existe
        Paciente = Paciente.query.get(patient_id)
        if not Paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        records = HistoriaClinica.query.filter_by(patient_id=patient_id).all()
        
        result = []
        for record in records:
            record_data = {
                'id': record.id,
                'patient_id': record.patient_id,
                'doctor_name': record.doctor_name,
                'visit_date': record.visit_date.isoformat() if record.visit_date else None,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'integrity_hash': record.integrity_hash
            }
            
            # Descifrar campos sensibles
            if record.symptoms:
                try:
                    record_data['symptoms'] = get_crypto_service().decrypt_aes(record.symptoms)
                except:
                    record_data['symptoms'] = None
            else:
                record_data['symptoms'] = None
                
            if record.diagnosis:
                try:
                    record_data['diagnosis'] = get_crypto_service().decrypt_aes(record.diagnosis)
                except:
                    record_data['diagnosis'] = None
            else:
                record_data['diagnosis'] = None
                
            if record.treatment:
                try:
                    record_data['treatment'] = get_crypto_service().decrypt_aes(record.treatment)
                except:
                    record_data['treatment'] = None
            else:
                record_data['treatment'] = None
                
            if record.notes:
                try:
                    record_data['notes'] = get_crypto_service().decrypt_aes(record.notes)
                except:
                    record_data['notes'] = None
            else:
                record_data['notes'] = None
            
            result.append(record_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@medical_record_bp.route('/', methods=['POST'])
@jwt_required()
def create_record():
    """Crear un nuevo registro médico"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['patient_id', 'doctor_name', 'visit_date', 'symptoms', 'diagnosis']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Verificar que el paciente existe
        Paciente = Paciente.query.get(data['patient_id'])
        if not Paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        # Cifrar campos sensibles
        encrypted_symptoms = get_crypto_service().encrypt_aes(data['symptoms'])
        encrypted_diagnosis = get_crypto_service().encrypt_aes(data['diagnosis'])
        
        encrypted_treatment = None
        if data.get('treatment'):
            encrypted_treatment = get_crypto_service().encrypt_aes(data['treatment'])
        
        encrypted_notes = None
        if data.get('notes'):
            encrypted_notes = get_crypto_service().encrypt_aes(data['notes'])
        
        # Crear registro médico
        record = HistoriaClinica(
            patient_id=data['patient_id'],
            doctor_name=data['doctor_name'],
            visit_date=datetime.fromisoformat(data['visit_date'].replace('Z', '+00:00')),
            symptoms=encrypted_symptoms,
            diagnosis=encrypted_diagnosis,
            treatment=encrypted_treatment,
            notes=encrypted_notes
        )
        
        # Calcular hash de integridad
        record_content = {
            'patient_id': record.patient_id,
            'doctor_name': record.doctor_name,
            'visit_date': record.visit_date.isoformat(),
            'symptoms': data['symptoms'],
            'diagnosis': data['diagnosis'],
            'treatment': data.get('treatment', ''),
            'notes': data.get('notes', '')
        }
        record.integrity_hash = get_crypto_service().hash_medical_record(record_content)
        
        db.session.add(record)
        db.session.commit()
        
        # Preparar respuesta
        response_data = {
            'id': record.id,
            'patient_id': record.patient_id,
            'doctor_name': record.doctor_name,
            'visit_date': record.visit_date.isoformat(),
            'symptoms': data['symptoms'],
            'diagnosis': data['diagnosis'],
            'treatment': data.get('treatment'),
            'notes': data.get('notes'),
            'integrity_hash': record.integrity_hash,
            'created_at': record.created_at.isoformat()
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@medical_record_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_record(id):
    """Obtener un registro médico por ID"""
    try:
        record = HistoriaClinica.query.get(id)
        
        if not record:
            return jsonify({'error': 'Registro médico no encontrado'}), 404
        
        record_data = {
            'id': record.id,
            'patient_id': record.patient_id,
            'doctor_name': record.doctor_name,
            'visit_date': record.visit_date.isoformat() if record.visit_date else None,
            'created_at': record.created_at.isoformat() if record.created_at else None,
            'integrity_hash': record.integrity_hash
        }
        
        # Descifrar campos sensibles
        if record.symptoms:
            try:
                record_data['symptoms'] = get_crypto_service().decrypt_aes(record.symptoms)
            except:
                record_data['symptoms'] = None
        else:
            record_data['symptoms'] = None
            
        if record.diagnosis:
            try:
                record_data['diagnosis'] = get_crypto_service().decrypt_aes(record.diagnosis)
            except:
                record_data['diagnosis'] = None
        else:
            record_data['diagnosis'] = None
            
        if record.treatment:
            try:
                record_data['treatment'] = get_crypto_service().decrypt_aes(record.treatment)
            except:
                record_data['treatment'] = None
        else:
            record_data['treatment'] = None
            
        if record.notes:
            try:
                record_data['notes'] = get_crypto_service().decrypt_aes(record.notes)
            except:
                record_data['notes'] = None
        else:
            record_data['notes'] = None
        
        # Verificar integridad
        record_content = {
            'patient_id': record.patient_id,
            'doctor_name': record.doctor_name,
            'visit_date': record.visit_date.isoformat() if record.visit_date else '',
            'symptoms': record_data.get('symptoms', ''),
            'diagnosis': record_data.get('diagnosis', ''),
            'treatment': record_data.get('treatment', ''),
            'notes': record_data.get('notes', '')
        }
        
        calculated_hash = get_crypto_service().hash_medical_record(record_content)
        record_data['integrity_verified'] = (calculated_hash == record.integrity_hash)
        
        return jsonify(record_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

