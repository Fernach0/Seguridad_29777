# SELECCIÓN DE BIBLIOTECAS CRIPTOGRÁFICAS
## ESPE MedSafe - Semana 2

---

## 1. RESUMEN DE BIBLIOTECAS SELECCIONADAS

```mermaid
mindmap
  root((Bibliotecas Python))
    Criptografía
      cryptography
        AES-256
        RSA-2048
        Padding
      hashlib
        SHA-256
        SHA-512
    Contraseñas
      bcrypt
        Hash
        Salt
        Factor de trabajo
    Web Framework
      Flask
        Flask-CORS
        Flask-JWT-Extended
      FastAPI alternativa
    Base de Datos
      SQLAlchemy
        ORM
        Migrations
      psycopg2
        PostgreSQL Driver
    Utilidades
      python-dotenv
        Variables de entorno
      validators
        Validación de datos
```

---

## 2. BIBLIOTECAS CRIPTOGRÁFICAS PRINCIPALES

### 2.1 `cryptography` (versión 41.0+)

**Propósito**: Biblioteca completa de criptografía moderna para Python.

#### Instalación:
```bash
pip install cryptography==41.0.5
```

#### Características:
✅ Implementa AES en múltiples modos (CBC, GCM, CFB)  
✅ Soporte completo para RSA  
✅ Generación de claves asimétricas  
✅ Padding schemes (OAEP, PSS)  
✅ Mantenida activamente por PyCA  
✅ Compatible con FIPS 140-2  

#### Uso en ESPE MedSafe:

**Cifrado AES-256-CBC:**
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_aes(plaintext: str, key: bytes) -> tuple:
    """
    Cifra texto con AES-256-CBC
    
    Args:
        plaintext: Texto a cifrar
        key: Clave de 32 bytes (256 bits)
    
    Returns:
        (ciphertext, iv): Texto cifrado e IV
    """
    iv = os.urandom(16)  # Vector de inicialización aleatorio
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    # Padding PKCS7
    from cryptography.hazmat.primitives import padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext, iv

def decrypt_aes(ciphertext: bytes, key: bytes, iv: bytes) -> str:
    """
    Descifra texto con AES-256-CBC
    
    Args:
        ciphertext: Texto cifrado
        key: Clave de 32 bytes
        iv: Vector de inicialización
    
    Returns:
        Texto descifrado
    """
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remover padding
    from cryptography.hazmat.primitives import padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext.decode()
```

**Cifrado RSA-2048:**
```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_rsa_keys():
    """Genera par de claves RSA-2048"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_rsa(plaintext: str, public_key) -> bytes:
    """Cifra texto con RSA"""
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_rsa(ciphertext: bytes, private_key) -> str:
    """Descifra texto con RSA"""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()
```

**Firma Digital RSA:**
```python
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def sign_data(data: str, private_key) -> bytes:
    """Firma datos con RSA"""
    signature = private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(data: str, signature: bytes, public_key) -> bool:
    """Verifica firma RSA"""
    try:
        public_key.verify(
            signature,
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
```

---

### 2.2 `bcrypt` (versión 4.1+)

**Propósito**: Hashing seguro de contraseñas con salt automático.

#### Instalación:
```bash
pip install bcrypt==4.1.2
```

#### Características:
✅ Salt automático por defecto  
✅ Factor de trabajo ajustable (cost factor)  
✅ Resistente a ataques con GPUs  
✅ Implementado en C (rápido)  
✅ Estándar de la industria  

#### Uso en ESPE MedSafe:

```python
import bcrypt

def hash_password(password: str) -> tuple:
    """
    Hashea una contraseña con bcrypt
    
    Args:
        password: Contraseña en texto plano
    
    Returns:
        (hash, salt): Hash y salt (el salt está incluido en el hash)
    """
    # Factor de trabajo: 12 (2^12 = 4096 iteraciones)
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode(), salt)
    return password_hash.decode(), salt.decode()

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica una contraseña contra su hash
    
    Args:
        password: Contraseña a verificar
        password_hash: Hash almacenado
    
    Returns:
        True si coincide, False si no
    """
    return bcrypt.checkpw(password.encode(), password_hash.encode())

# Ejemplo de uso:
password = "Doctor123!"
hashed, salt = hash_password(password)
print(f"Hash: {hashed}")
print(f"Verificación correcta: {verify_password('Doctor123!', hashed)}")
print(f"Verificación incorrecta: {verify_password('wrong', hashed)}")
```

**Salida esperada:**
```
Hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqXQ8kN7Hy
Verificación correcta: True
Verificación incorrecta: False
```

**Nota importante**: El salt está incluido en el hash de bcrypt, por lo que no es necesario almacenarlo por separado. Sin embargo, en nuestro modelo de BD lo incluimos para fines educativos.

---

### 2.3 `hashlib` (biblioteca estándar)

**Propósito**: Funciones hash criptográficas (SHA-256, SHA-512, etc.).

#### Instalación:
```bash
# Ya viene con Python, no requiere instalación
```

#### Características:
✅ Parte de la biblioteca estándar de Python  
✅ Soporta SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA3  
✅ Rápido y eficiente  
✅ Implementado en C  

#### Uso en ESPE MedSafe:

```python
import hashlib
import json

def calculate_sha256(data: str) -> str:
    """
    Calcula hash SHA-256 de un texto
    
    Args:
        data: Texto a hashear
    
    Returns:
        Hash en formato hexadecimal
    """
    return hashlib.sha256(data.encode()).hexdigest()

def verify_integrity(original_data: dict, stored_hash: str) -> bool:
    """
    Verifica la integridad de datos usando SHA-256
    
    Args:
        original_data: Datos actuales
        stored_hash: Hash almacenado previamente
    
    Returns:
        True si no ha sido modificado, False si hay cambios
    """
    # Concatenar campos relevantes
    data_string = json.dumps(original_data, sort_keys=True)
    calculated_hash = calculate_sha256(data_string)
    return calculated_hash == stored_hash

# Ejemplo para historias clínicas:
def hash_medical_record(sintomas: str, diagnostico: str, 
                        tratamiento: str, notas: str,
                        timestamp: str) -> str:
    """
    Calcula hash de integridad de una historia clínica
    """
    data = f"{sintomas}|{diagnostico}|{tratamiento}|{notas}|{timestamp}"
    return calculate_sha256(data)

# Uso:
hash_integridad = hash_medical_record(
    "Fiebre alta",
    "Faringitis aguda",
    "Reposo y antibióticos",
    "Mejoría esperada en 3 días",
    "2026-01-08 11:30:00"
)
print(f"Hash de integridad: {hash_integridad}")
```

---

## 3. BIBLIOTECAS DE DESARROLLO WEB

### 3.1 Flask (versión 3.0+)

```bash
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install Flask-JWT-Extended==4.6.0
```

**Extensiones necesarias:**

- **Flask-CORS**: Manejo de CORS (Cross-Origin Resource Sharing)
- **Flask-JWT-Extended**: Autenticación con JWT

#### Ejemplo de configuración:

```python
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'tu-clave-secreta-aqui'  # Cambiar en producción
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1800  # 30 minutos

CORS(app)
jwt = JWTManager(app)

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    # Lógica de autenticación
    access_token = create_access_token(identity=user_id)
    return jsonify({"token": access_token}), 200
```

---

### 3.2 Alternativa: FastAPI (versión 0.109+)

```bash
pip install fastapi==0.109.0
pip install uvicorn[standard]==0.27.0
pip install python-jose[cryptography]==3.3.0
```

**Ventajas de FastAPI:**
- Más rápido que Flask
- Validación automática con Pydantic
- Documentación automática (Swagger)
- Tipado estático nativo

#### Ejemplo de configuración:

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ESPE MedSafe API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.post("/api/v1/auth/login")
async def login(credentials: LoginSchema):
    # Lógica de autenticación
    token = create_jwt_token(user_id)
    return {"token": token}
```

**Recomendación**: **Flask** para simplicidad, **FastAPI** para rendimiento y escalabilidad.

---

## 4. BIBLIOTECAS DE BASE DE DATOS

### 4.1 SQLAlchemy (versión 2.0+)

```bash
pip install SQLAlchemy==2.0.25
```

**ORM para interacción con la base de datos:**

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(32), nullable=False)
    rol = Column(String(20), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    cedula = Column(String(10), unique=True, nullable=False)
    activo = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

# Crear conexión
engine = create_engine('postgresql://user:password@localhost/espe_medsafe')
Session = sessionmaker(bind=engine)
session = Session()
```

---

### 4.2 psycopg2 (PostgreSQL Driver)

```bash
pip install psycopg2-binary==2.9.9
```

**Conector para PostgreSQL:**

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="espe_medsafe",
    user="postgres",
    password="tu_password"
)
```

**Alternativa para MySQL:**
```bash
pip install PyMySQL==1.1.0
```

---

## 5. BIBLIOTECAS AUXILIARES

### 5.1 `python-dotenv` (versión 1.0+)

```bash
pip install python-dotenv==1.0.0
```

**Gestión de variables de entorno:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
AES_KEY = os.getenv("AES_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")
```

**Archivo `.env`:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=espe_medsafe
DB_USER=postgres
DB_PASSWORD=tu_password_seguro

AES_KEY=clave_de_32_bytes_en_base64_aqui==
JWT_SECRET=tu_clave_jwt_secreta_aqui
JWT_EXPIRATION=1800

FLASK_ENV=development
FLASK_DEBUG=True
```

---

### 5.2 `validators` (versión 0.22+)

```bash
pip install validators==0.22.0
```

**Validación de datos:**

```python
import validators

def validate_email(email: str) -> bool:
    return validators.email(email)

def validate_cedula(cedula: str) -> bool:
    return cedula.isdigit() and len(cedula) == 10
```

---

## 6. ARCHIVO `requirements.txt` COMPLETO

```txt
# ============================================
# ESPE MedSafe - Dependencias Python
# ============================================

# Framework Web
Flask==3.0.0
Flask-CORS==4.0.0
Flask-JWT-Extended==4.6.0
gunicorn==21.2.0

# Base de Datos
SQLAlchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Criptografía
cryptography==41.0.5
bcrypt==4.1.2

# Utilidades
python-dotenv==1.0.0
validators==0.22.0
python-dateutil==2.8.2

# Testing (Opcional)
pytest==7.4.4
pytest-cov==4.1.0

# Documentación (Opcional)
Flask-Swagger-UI==4.11.1
```

---

## 7. INSTALACIÓN Y CONFIGURACIÓN

### 7.1 Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### 7.2 Generación de Claves

```python
# Generar clave AES-256 (32 bytes)
import os
import base64

aes_key = base64.b64encode(os.urandom(32)).decode()
print(f"AES_KEY={aes_key}")

# Generar clave JWT
jwt_secret = base64.b64encode(os.urandom(64)).decode()
print(f"JWT_SECRET={jwt_secret}")
```

---

## 8. COMPARACIÓN DE ALTERNATIVAS

| Característica | cryptography | PyCryptodome | hashlib | bcrypt |
|----------------|--------------|--------------|---------|--------|
| AES | ✅ | ✅ | ❌ | ❌ |
| RSA | ✅ | ✅ | ❌ | ❌ |
| SHA-256 | ✅ | ✅ | ✅ | ❌ |
| bcrypt hash | ❌ | ❌ | ❌ | ✅ |
| Mantenimiento activo | ✅ | ✅ | ✅ | ✅ |
| Documentación | Excelente | Buena | Buena | Buena |
| Velocidad | Rápida | Rápida | Muy rápida | Lenta (intencionalmente) |

**Decisión**: Usar **cryptography** + **bcrypt** + **hashlib** (las tres juntas cubren todas las necesidades).

---

## 9. PRUEBAS UNITARIAS

```python
# tests/test_crypto.py
import pytest
from services.crypto_service import encrypt_aes, decrypt_aes, hash_password, verify_password

def test_aes_encryption():
    key = os.urandom(32)
    plaintext = "Este es un mensaje secreto"
    
    ciphertext, iv = encrypt_aes(plaintext, key)
    decrypted = decrypt_aes(ciphertext, key, iv)
    
    assert decrypted == plaintext

def test_bcrypt_hashing():
    password = "Doctor123!"
    hashed, salt = hash_password(password)
    
    assert verify_password("Doctor123!", hashed) == True
    assert verify_password("wrong", hashed) == False

def test_sha256_integrity():
    data = "Historia clínica #123"
    hash1 = calculate_sha256(data)
    hash2 = calculate_sha256(data)
    
    assert hash1 == hash2  # Hash debe ser determinístico
```

---

## 10. SEGURIDAD EN PRODUCCIÓN

### ✅ Mejores Prácticas:

1. **Variables de entorno**: Nunca hardcodear claves en el código
2. **Rotación de claves**: Cambiar claves periódicamente
3. **Logging**: NO registrar claves ni contraseñas en logs
4. **Dependencias**: Mantener bibliotecas actualizadas
5. **Auditoría**: Revisar vulnerabilidades conocidas (CVE)

### 🔒 Almacenamiento de Claves:

```python
# ❌ MAL - Clave hardcodeada
AES_KEY = b'this_is_a_very_secret_key_123456'

# ✅ BIEN - Clave desde variable de entorno
AES_KEY = base64.b64decode(os.getenv('AES_KEY'))

# ✅ MEJOR - Usar un gestor de secretos
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url="https://...", credential=credential)
AES_KEY = client.get_secret("aes-key").value
```

---

**Fecha**: 8 de enero de 2026  
**Equipo**: ESPE MedSafe  
**Semana**: 2 - Selección de Bibliotecas Criptográficas
