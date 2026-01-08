"""
Servicio de Criptografía - ESPE MedSafe
Implementa AES-256, RSA-2048, bcrypt, SHA-256
"""
import os
import base64
import hashlib
import bcrypt
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend


class CryptoService:
    """Servicio centralizado de operaciones criptográficas"""
    
    def __init__(self, master_key: Optional[str] = None):
        """
        Inicializar servicio criptográfico
        
        Args:
            master_key: Clave maestra AES en base64 (32 bytes)
        """
        if master_key:
            self.master_key = base64.b64decode(master_key)
        else:
            # Generar clave temporal (solo para desarrollo)
            self.master_key = os.urandom(32)
    
    # ==========================================
    # CIFRADO SIMÉTRICO - AES-256-CBC
    # ==========================================
    
    def encrypt_aes(self, plaintext: str) -> Tuple[bytes, bytes]:
        """
        Cifrar texto con AES-256-CBC
        
        Args:
            plaintext: Texto a cifrar
            
        Returns:
            (ciphertext, iv): Texto cifrado y vector de inicialización
        """
        # Generar IV aleatorio (16 bytes)
        iv = os.urandom(16)
        
        # Crear cipher AES-256-CBC
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Aplicar padding PKCS7
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        
        # Cifrar
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return ciphertext, iv
    
    def decrypt_aes(self, ciphertext: bytes, iv: bytes) -> str:
        """
        Descifrar texto con AES-256-CBC
        
        Args:
            ciphertext: Texto cifrado
            iv: Vector de inicialización usado en el cifrado
            
        Returns:
            Texto descifrado
        """
        # Crear cipher AES-256-CBC
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Descifrar
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remover padding PKCS7
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')
    
    # ==========================================
    # CIFRADO ASIMÉTRICO - RSA-2048
    # ==========================================
    
    def generate_rsa_keys(self) -> Tuple[bytes, bytes]:
        """
        Generar par de claves RSA-2048
        
        Returns:
            (private_key_pem, public_key_pem): Claves en formato PEM
        """
        # Generar clave privada RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Obtener clave pública
        public_key = private_key.public_key()
        
        # Serializar a formato PEM
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def encrypt_rsa(self, plaintext: str, public_key_pem: bytes) -> bytes:
        """
        Cifrar texto con RSA-2048
        
        Args:
            plaintext: Texto a cifrar (máximo ~200 caracteres para RSA-2048)
            public_key_pem: Clave pública en formato PEM
            
        Returns:
            Texto cifrado
        """
        # Cargar clave pública
        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )
        
        # Cifrar con OAEP padding
        ciphertext = public_key.encrypt(
            plaintext.encode('utf-8'),
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return ciphertext
    
    def decrypt_rsa(self, ciphertext: bytes, private_key_pem: bytes) -> str:
        """
        Descifrar texto con RSA-2048
        
        Args:
            ciphertext: Texto cifrado
            private_key_pem: Clave privada en formato PEM
            
        Returns:
            Texto descifrado
        """
        # Cargar clave privada
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )
        
        # Descifrar con OAEP padding
        plaintext = private_key.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return plaintext.decode('utf-8')
    
    def sign_rsa(self, data: str, private_key_pem: bytes) -> bytes:
        """
        Firmar datos con RSA-2048
        
        Args:
            data: Datos a firmar
            private_key_pem: Clave privada en formato PEM
            
        Returns:
            Firma digital
        """
        # Cargar clave privada
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=default_backend()
        )
        
        # Firmar con PSS padding
        signature = private_key.sign(
            data.encode('utf-8'),
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return signature
    
    def verify_signature_rsa(self, data: str, signature: bytes, 
                           public_key_pem: bytes) -> bool:
        """
        Verificar firma digital RSA
        
        Args:
            data: Datos originales
            signature: Firma a verificar
            public_key_pem: Clave pública en formato PEM
            
        Returns:
            True si la firma es válida, False si no
        """
        try:
            # Cargar clave pública
            public_key = serialization.load_pem_public_key(
                public_key_pem,
                backend=default_backend()
            )
            
            # Verificar firma
            public_key.verify(
                signature,
                data.encode('utf-8'),
                asym_padding.PSS(
                    mgf=asym_padding.MGF1(hashes.SHA256()),
                    salt_length=asym_padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    # ==========================================
    # HASH DE CONTRASEÑAS - bcrypt
    # ==========================================
    
    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        """
        Hashear contraseña con bcrypt
        
        Args:
            password: Contraseña en texto plano
            rounds: Factor de trabajo (default: 12 = 2^12 = 4096 iteraciones)
            
        Returns:
            Hash de la contraseña (incluye el salt)
        """
        # Generar salt y hashear
        salt = bcrypt.gensalt(rounds=rounds)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        return password_hash.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verificar contraseña contra su hash
        
        Args:
            password: Contraseña a verificar
            password_hash: Hash almacenado
            
        Returns:
            True si la contraseña es correcta, False si no
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception:
            return False
    
    # ==========================================
    # HASH DE INTEGRIDAD - SHA-256
    # ==========================================
    
    @staticmethod
    def calculate_sha256(data: str) -> str:
        """
        Calcular hash SHA-256 de datos
        
        Args:
            data: Datos a hashear
            
        Returns:
            Hash en formato hexadecimal
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_integrity(data: str, stored_hash: str) -> bool:
        """
        Verificar integridad de datos usando SHA-256
        
        Args:
            data: Datos actuales
            stored_hash: Hash almacenado previamente
            
        Returns:
            True si no ha sido modificado, False si hay cambios
        """
        current_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
        return current_hash == stored_hash
    
    @staticmethod
    def hash_medical_record(sintomas: str, diagnostico: str, 
                          tratamiento: str, notas: str, 
                          fecha_consulta: str) -> str:
        """
        Calcular hash de integridad de una historia clínica
        
        Args:
            sintomas: Síntomas del paciente
            diagnostico: Diagnóstico médico
            tratamiento: Plan de tratamiento
            notas: Notas adicionales
            fecha_consulta: Fecha de la consulta
            
        Returns:
            Hash SHA-256 en hexadecimal
        """
        # Concatenar campos en orden específico
        data = f"{sintomas}|{diagnostico}|{tratamiento}|{notas}|{fecha_consulta}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    # ==========================================
    # CIFRADOS CLÁSICOS (Educativo)
    # ==========================================
    
    @staticmethod
    def caesar_cipher(text: str, shift: int, encrypt: bool = True) -> str:
        """
        Cifrado César
        
        Args:
            text: Texto a cifrar/descifrar
            shift: Desplazamiento (1-25)
            encrypt: True para cifrar, False para descifrar
            
        Returns:
            Texto cifrado/descifrado
        """
        if not encrypt:
            shift = -shift
        
        result = []
        for char in text.upper():
            if char.isalpha():
                # Desplazar letra
                shifted = chr(((ord(char) - 65 + shift) % 26) + 65)
                result.append(shifted)
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def vigenere_cipher(text: str, key: str, encrypt: bool = True) -> str:
        """
        Cifrado Vigenère
        
        Args:
            text: Texto a cifrar/descifrar
            key: Palabra clave
            encrypt: True para cifrar, False para descifrar
            
        Returns:
            Texto cifrado/descifrado
        """
        text = text.upper()
        key = key.upper()
        result = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                # Obtener valor de la clave
                key_char = key[key_index % len(key)]
                key_value = ord(key_char) - 65
                
                if not encrypt:
                    key_value = -key_value
                
                # Cifrar/descifrar
                shifted = chr(((ord(char) - 65 + key_value) % 26) + 65)
                result.append(shifted)
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)


# Instancia global del servicio
crypto_service = None


def init_crypto_service(master_key: str):
    """
    Inicializar servicio criptográfico global
    
    Args:
        master_key: Clave maestra AES en base64
    """
    global crypto_service
    crypto_service = CryptoService(master_key)
    return crypto_service


def get_crypto_service():
    """
    Obtener instancia del servicio criptográfico
    Inicializa automáticamente si no existe
    
    Returns:
        CryptoService: Instancia del servicio
    """
    global crypto_service
    
    if crypto_service is None:
        # Auto-inicializar con clave del entorno
        from flask import current_app
        try:
            aes_key = current_app.config.get('AES_MASTER_KEY')
            if not aes_key:
                # Usar clave por defecto para desarrollo
                aes_key = os.environ.get('AES_MASTER_KEY')
            
            if aes_key:
                crypto_service = CryptoService(aes_key)
            else:
                # Última opción: clave temporal
                print("⚠️  Inicializando crypto_service con clave temporal")
                crypto_service = CryptoService(base64.b64encode(os.urandom(32)).decode())
        except:
            # Si no hay contexto de Flask, usar variable de entorno
            aes_key = os.environ.get('AES_MASTER_KEY')
            if aes_key:
                crypto_service = CryptoService(aes_key)
            else:
                crypto_service = CryptoService(base64.b64encode(os.urandom(32)).decode())
    
    return crypto_service
