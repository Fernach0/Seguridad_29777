from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.crypto_service import get_crypto_service

crypto_bp = Blueprint('crypto_bp', __name__, url_prefix='/api/v1/crypto')


# ==================== AES Encryption/Decryption ====================

@crypto_bp.route('/aes/encrypt', methods=['POST'])
@jwt_required()
def aes_encrypt():
    """Demo: Cifrar texto con AES"""
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'Campo requerido: text'}), 400
        
        encrypted = get_crypto_service().encrypt_aes(data['text'])
        
        return jsonify({
            'original': data['text'],
            'encrypted': encrypted,
            'algorithm': 'AES-256-CBC'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crypto_bp.route('/aes/decrypt', methods=['POST'])
@jwt_required()
def aes_decrypt():
    """Demo: Descifrar texto con AES"""
    try:
        data = request.get_json()
        
        if 'encrypted_text' not in data:
            return jsonify({'error': 'Campo requerido: encrypted_text'}), 400
        
        decrypted = get_crypto_service().decrypt_aes(data['encrypted_text'])
        
        return jsonify({
            'encrypted': data['encrypted_text'],
            'decrypted': decrypted,
            'algorithm': 'AES-256-CBC'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== RSA Encryption/Decryption ====================

@crypto_bp.route('/rsa/generate', methods=['POST'])
@jwt_required()
def rsa_generate():
    """Demo: Generar par de llaves RSA"""
    try:
        data = request.get_json()
        key_size = data.get('key_size', 2048)
        
        if key_size not in [1024, 2048, 4096]:
            return jsonify({'error': 'key_size debe ser 1024, 2048 o 4096'}), 400
        
        public_key, private_key = get_crypto_service().generate_rsa_key_pair(key_size)
        
        return jsonify({
            'public_key': public_key,
            'private_key': private_key,
            'key_size': key_size,
            'algorithm': 'RSA'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crypto_bp.route('/rsa/encrypt', methods=['POST'])
@jwt_required()
def rsa_encrypt():
    """Demo: Cifrar texto con RSA"""
    try:
        data = request.get_json()
        
        if 'text' not in data or 'public_key' not in data:
            return jsonify({'error': 'Campos requeridos: text, public_key'}), 400
        
        encrypted = get_crypto_service().encrypt_rsa(data['text'], data['public_key'])
        
        return jsonify({
            'original': data['text'],
            'encrypted': encrypted,
            'algorithm': 'RSA'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crypto_bp.route('/rsa/decrypt', methods=['POST'])
@jwt_required()
def rsa_decrypt():
    """Demo: Descifrar texto con RSA"""
    try:
        data = request.get_json()
        
        if 'encrypted_text' not in data or 'private_key' not in data:
            return jsonify({'error': 'Campos requeridos: encrypted_text, private_key'}), 400
        
        decrypted = get_crypto_service().decrypt_rsa(data['encrypted_text'], data['private_key'])
        
        return jsonify({
            'encrypted': data['encrypted_text'],
            'decrypted': decrypted,
            'algorithm': 'RSA'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Hash Functions ====================

@crypto_bp.route('/hash/sha256', methods=['POST'])
@jwt_required()
def hash_sha256():
    """Demo: Calcular hash SHA-256"""
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'Campo requerido: text'}), 400
        
        hash_value = get_crypto_service().hash_sha256(data['text'])
        
        return jsonify({
            'original': data['text'],
            'hash': hash_value,
            'algorithm': 'SHA-256'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crypto_bp.route('/hash/verify', methods=['POST'])
@jwt_required()
def verify_hash():
    """Demo: Verificar hash SHA-256"""
    try:
        data = request.get_json()
        
        if 'text' not in data or 'hash' not in data:
            return jsonify({'error': 'Campos requeridos: text, hash'}), 400
        
        calculated_hash = get_crypto_service().hash_sha256(data['text'])
        is_valid = calculated_hash == data['hash']
        
        return jsonify({
            'text': data['text'],
            'provided_hash': data['hash'],
            'calculated_hash': calculated_hash,
            'is_valid': is_valid,
            'algorithm': 'SHA-256'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Password Hashing ====================

@crypto_bp.route('/password/hash', methods=['POST'])
@jwt_required()
def hash_password():
    """Demo: Hash de contraseña con bcrypt"""
    try:
        data = request.get_json()
        
        if 'password' not in data:
            return jsonify({'error': 'Campo requerido: password'}), 400
        
        hashed = get_crypto_service().hash_password(data['password'])
        
        return jsonify({
            'password': data['password'],
            'hashed': hashed,
            'algorithm': 'bcrypt'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crypto_bp.route('/password/verify', methods=['POST'])
@jwt_required()
def verify_password():
    """Demo: Verificar contraseña con bcrypt"""
    try:
        data = request.get_json()
        
        if 'password' not in data or 'hashed' not in data:
            return jsonify({'error': 'Campos requeridos: password, hashed'}), 400
        
        is_valid = get_crypto_service().verify_password(data['password'], data['hashed'])
        
        return jsonify({
            'password': data['password'],
            'hashed': data['hashed'],
            'is_valid': is_valid,
            'algorithm': 'bcrypt'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== Classic Ciphers ====================

@crypto_bp.route('/classic/caesar', methods=['POST'])
@jwt_required()
def caesar_cipher():
    """Demo: Cifrado César"""
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'Campo requerido: text'}), 400
        
        shift = data.get('shift', 3)
        operation = data.get('operation', 'encrypt')  # 'encrypt' o 'decrypt'
        
        if operation == 'decrypt':
            shift = -shift
        
        result = get_crypto_service().caesar_cipher(data['text'], shift)
        
        return jsonify({
            'original': data['text'],
            'result': result,
            'shift': abs(shift),
            'operation': operation,
            'algorithm': 'Caesar Cipher'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@crypto_bp.route('/classic/vigenere', methods=['POST'])
@jwt_required()
def vigenere_cipher():
    """Demo: Cifrado Vigenère"""
    try:
        data = request.get_json()
        
        if 'text' not in data or 'key' not in data:
            return jsonify({'error': 'Campos requeridos: text, key'}), 400
        
        operation = data.get('operation', 'encrypt')  # 'encrypt' o 'decrypt'
        
        result = get_crypto_service().vigenere_cipher(
            data['text'], 
            data['key'], 
            operation == 'decrypt'
        )
        
        return jsonify({
            'original': data['text'],
            'result': result,
            'key': data['key'],
            'operation': operation,
            'algorithm': 'Vigenère Cipher'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
