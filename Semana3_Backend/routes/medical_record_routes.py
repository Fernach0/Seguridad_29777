from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.medical_record import HistoriaClinica
from models.patient import Paciente
from models.user import Usuario
from models.base import db
from services.crypto_service import get_crypto_service
from datetime import datetime
import json

medical_record_bp = Blueprint('medical_record_bp', __name__, url_prefix='/api/v1/medical-records')


@medical_record_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_records():
    """Obtener todas las historias clínicas"""
    try:
        records = HistoriaClinica.query.all()
        
        result = []
        for record in records:
            record_data = {
                'id': record.id,
                'paciente_id': record.paciente_id,
                'doctor_id': record.doctor_id,
                'fecha_consulta': record.fecha_consulta.isoformat() if record.fecha_consulta else None,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'hash_integridad': record.hash_integridad
            }
            
            # Descifrar campos sensibles usando el mismo IV
            if record.sintomas_encrypted and record.iv_aes:
                try:
                    record_data['sintomas'] = get_crypto_service().decrypt_aes(
                        record.sintomas_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando síntomas: {e}")
                    record_data['sintomas'] = None
            else:
                record_data['sintomas'] = None
                
            if record.diagnostico_encrypted and record.iv_aes:
                try:
                    record_data['diagnostico'] = get_crypto_service().decrypt_aes(
                        record.diagnostico_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando diagnóstico: {e}")
                    record_data['diagnostico'] = None
            else:
                record_data['diagnostico'] = None
                
            if record.tratamiento_encrypted and record.iv_aes:
                try:
                    record_data['tratamiento'] = get_crypto_service().decrypt_aes(
                        record.tratamiento_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando tratamiento: {e}")
                    record_data['tratamiento'] = None
            else:
                record_data['tratamiento'] = None
                
            if record.notas_encrypted and record.iv_aes:
                try:
                    record_data['notas'] = get_crypto_service().decrypt_aes(
                        record.notas_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando notas: {e}")
                    record_data['notas'] = None
            else:
                record_data['notas'] = None
            
            result.append(record_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo todas las historias clínicas: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@medical_record_bp.route('/paciente/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_records(patient_id):
    """Obtener todos los registros médicos de un paciente"""
    try:
        # Verificar que el paciente existe
        paciente = Paciente.query.get(patient_id)
        if not paciente:
            return jsonify({'error': 'Paciente no encontrado'}), 404
        
        records = HistoriaClinica.query.filter_by(paciente_id=patient_id).all()
        
        result = []
        for record in records:
            record_data = {
                'id': record.id,
                'paciente_id': record.paciente_id,
                'doctor_id': record.doctor_id,
                'fecha_consulta': record.fecha_consulta.isoformat() if record.fecha_consulta else None,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'hash_integridad': record.hash_integridad
            }
            
            # Descifrar campos sensibles usando el mismo IV
            if record.sintomas_encrypted and record.iv_aes:
                try:
                    record_data['sintomas'] = get_crypto_service().decrypt_aes(
                        record.sintomas_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando síntomas: {e}")
                    record_data['sintomas'] = None
            else:
                record_data['sintomas'] = None
                
            if record.diagnostico_encrypted and record.iv_aes:
                try:
                    record_data['diagnostico'] = get_crypto_service().decrypt_aes(
                        record.diagnostico_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando diagnóstico: {e}")
                    record_data['diagnostico'] = None
            else:
                record_data['diagnostico'] = None
                
            if record.tratamiento_encrypted and record.iv_aes:
                try:
                    record_data['tratamiento'] = get_crypto_service().decrypt_aes(
                        record.tratamiento_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando tratamiento: {e}")
                    record_data['tratamiento'] = None
            else:
                record_data['tratamiento'] = None
                
            if record.notas_encrypted and record.iv_aes:
                try:
                    record_data['notas'] = get_crypto_service().decrypt_aes(
                        record.notas_encrypted,
                        record.iv_aes
                    )
                except Exception as e:
                    print(f"⚠️  Error descifrando notas: {e}")
                    record_data['notas'] = None
            else:
                record_data['notas'] = None
            
            result.append(record_data)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo historias clínicas: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@medical_record_bp.route('/', methods=['POST'])
@jwt_required()
def create_record():
    """Crear un nuevo registro médico"""
    try:
        data = request.get_json()
        claims = get_jwt()
        doctor_id = int(get_jwt_identity())
        
        # Validar campos requeridos
        required_fields = ['paciente_id', 'fecha_consulta', 'sintomas', 'diagnostico']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Verificar que el paciente existe
        paciente = Paciente.query.get(data['paciente_id'])
        if not paciente:
            return jsonify({
                'success': False,
                'error': 'Paciente no encontrado'
            }), 404
        
        # Generar un IV único para este registro y usarlo para todos los campos
        sintomas_encrypted, iv = get_crypto_service().encrypt_aes(data['sintomas'])
        diagnostico_encrypted, _ = get_crypto_service().encrypt_aes(data['diagnostico'], iv)
        
        tratamiento_encrypted = None
        if data.get('tratamiento'):
            tratamiento_encrypted, _ = get_crypto_service().encrypt_aes(data['tratamiento'], iv)
        
        notas_encrypted = None
        if data.get('notas'):
            notas_encrypted, _ = get_crypto_service().encrypt_aes(data['notas'], iv)
        
        # Calcular hash de integridad
        record_content = {
            'paciente_id': data['paciente_id'],
            'doctor_id': doctor_id,
            'fecha_consulta': data['fecha_consulta'],
            'sintomas': data['sintomas'],
            'diagnostico': data['diagnostico'],
            'tratamiento': data.get('tratamiento', ''),
            'notas': data.get('notas', '')
        }
        hash_integridad = get_crypto_service().calculate_sha256(json.dumps(record_content, sort_keys=True))
        
        # Crear registro médico
        record = HistoriaClinica(
            paciente_id=data['paciente_id'],
            doctor_id=doctor_id,
            fecha_consulta=datetime.fromisoformat(data['fecha_consulta'].replace('Z', '+00:00')).date(),
            sintomas_encrypted=sintomas_encrypted,
            diagnostico_encrypted=diagnostico_encrypted,
            tratamiento_encrypted=tratamiento_encrypted,
            notas_encrypted=notas_encrypted,
            iv_aes=iv,
            hash_integridad=hash_integridad
        )
        
        db.session.add(record)
        db.session.commit()
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'data': {
                'id': record.id,
                'paciente_id': record.paciente_id,
                'doctor_id': record.doctor_id,
                'fecha_consulta': record.fecha_consulta.isoformat(),
                'sintomas': data['sintomas'],
                'diagnostico': data['diagnostico'],
                'tratamiento': data.get('tratamiento'),
                'notas': data.get('notas'),
                'hash_integridad': record.hash_integridad,
                'created_at': record.created_at.isoformat()
            },
            'message': 'Historia clínica creada exitosamente'
        }
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creando historia clínica: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Error en el servidor',
            'details': str(e)
        }), 500


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
            'paciente_id': record.paciente_id,
            'doctor_id': record.doctor_id,
            'fecha_consulta': record.fecha_consulta.isoformat() if record.fecha_consulta else None,
            'created_at': record.created_at.isoformat() if record.created_at else None,
            'hash_integridad': record.hash_integridad
        }
        
        # Descifrar campos sensibles
        if record.sintomas_encrypted and record.iv_aes:
            try:
                record_data['sintomas'] = get_crypto_service().decrypt_aes(
                    record.sintomas_encrypted,
                    record.iv_aes
                )
            except Exception as e:
                print(f"⚠️  Error descifrando síntomas: {e}")
                record_data['sintomas'] = None
        else:
            record_data['sintomas'] = None
            
        if record.diagnostico_encrypted and record.iv_aes:
            try:
                record_data['diagnostico'] = get_crypto_service().decrypt_aes(
                    record.diagnostico_encrypted,
                    record.iv_aes
                )
            except Exception as e:
                print(f"⚠️  Error descifrando diagnóstico: {e}")
                record_data['diagnostico'] = None
        else:
            record_data['diagnostico'] = None
            
        if record.tratamiento_encrypted and record.iv_aes:
            try:
                record_data['tratamiento'] = get_crypto_service().decrypt_aes(
                    record.tratamiento_encrypted,
                    record.iv_aes
                )
            except Exception as e:
                print(f"⚠️  Error descifrando tratamiento: {e}")
                record_data['tratamiento'] = None
        else:
            record_data['tratamiento'] = None
            
        if record.notas_encrypted and record.iv_aes:
            try:
                record_data['notas'] = get_crypto_service().decrypt_aes(
                    record.notas_encrypted,
                    record.iv_aes
                )
            except Exception as e:
                print(f"⚠️  Error descifrando notas: {e}")
                record_data['notas'] = None
        else:
            record_data['notas'] = None
        
        # Verificar integridad
        record_content = {
            'paciente_id': record.paciente_id,
            'doctor_id': record.doctor_id,
            'fecha_consulta': record.fecha_consulta.isoformat() if record.fecha_consulta else '',
            'sintomas': record_data.get('sintomas', ''),
            'diagnostico': record_data.get('diagnostico', ''),
            'tratamiento': record_data.get('tratamiento', ''),
            'notas': record_data.get('notas', '')
        }
        
        calculated_hash = get_crypto_service().calculate_sha256(json.dumps(record_content, sort_keys=True))
        record_data['integrity_verified'] = (calculated_hash == record.hash_integridad)
        
        return jsonify(record_data), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo historia clínica {id}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

