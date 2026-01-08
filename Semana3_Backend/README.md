# Backend ESPE MedSafe

Backend desarrollado con Flask para el sistema de gestión de historias clínicas ESPE MedSafe.

## 🔐 Características de Seguridad

### Técnicas Criptográficas Implementadas

1. **AES-256 (Cifrado Simétrico)**
   - Cifrado de datos médicos sensibles
   - Modo CBC con IV aleatorio
   - Padding PKCS7

2. **RSA-2048 (Cifrado Asimétrico)**
   - Generación de pares de claves
   - Cifrado con OAEP
   - Firmas digitales con PSS

3. **bcrypt (Hash de Contraseñas)**
   - Factor de trabajo: 12
   - Salt aleatorio por contraseña
   - Resistente a ataques de fuerza bruta

4. **SHA-256 (Verificación de Integridad)**
   - Hash de historias clínicas
   - Detección de modificaciones no autorizadas

5. **Cifrados Clásicos (Educativos)**
   - Cifrado César
   - Cifrado Vigenère

## 📁 Estructura del Proyecto

```
Semana3_Backend/
├── app.py                  # Punto de entrada de la aplicación
├── config.py               # Configuraciones
├── requirements.txt        # Dependencias
├── .env.example           # Variables de entorno de ejemplo
├── models/                # Modelos de datos
│   ├── __init__.py
│   ├── base.py
│   ├── user.py
│   ├── patient.py
│   ├── medical_record.py
│   ├── audit_log.py
│   └── rsa_key.py
├── routes/                # Endpoints REST API
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── patient_routes.py
│   ├── medical_record_routes.py
│   ├── audit_routes.py
│   └── crypto_routes.py
├── services/              # Lógica de negocio
│   ├── __init__.py
│   ├── crypto_service.py
│   └── auth_service.py
└── utils/                 # Utilidades
    ├── __init__.py
    ├── validators.py
    └── helpers.py
```

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15 o superior
- pip (gestor de paquetes de Python)

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

```bash
# Crear base de datos en PostgreSQL
createdb espe_medsafe

# O usando psql
psql -U postgres
CREATE DATABASE espe_medsafe;
\q
```

### 5. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Editar `.env`:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=espe_medsafe
DB_USER=postgres
DB_PASSWORD=tu_contraseña

# Flask
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=tu_clave_secreta_muy_segura

# JWT
JWT_SECRET_KEY=tu_jwt_secret_muy_seguro

# Criptografía - Generar con el comando siguiente
AES_MASTER_KEY=tu_clave_aes_base64
```

### 6. Generar Clave AES Maestra

```bash
python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
```

Copiar el resultado en `AES_MASTER_KEY` del archivo `.env`.

### 7. Crear Tablas de Base de Datos

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Tablas creadas exitosamente')"
```

### 8. Ejecutar Aplicación

#### Modo Desarrollo

```bash
python app.py
```

#### Modo Producción

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

La API estará disponible en: `http://localhost:5000`

## 📚 Documentación de la API

### Base URL

```
http://localhost:5000/api/v1
```

### Autenticación

La API usa JWT (JSON Web Tokens) para autenticación. Después del login, incluir el token en el header:

```
Authorization: Bearer <tu_token_jwt>
```

### Endpoints Principales

#### 1. Autenticación (`/auth`)

- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener usuario actual (requiere token)
- `POST /auth/logout` - Cerrar sesión (requiere token)

#### 2. Usuarios (`/users`) - Solo Admin

- `GET /users` - Listar usuarios
- `GET /users/<id>` - Obtener usuario por ID
- `POST /users` - Crear usuario
- `PUT /users/<id>` - Actualizar usuario
- `DELETE /users/<id>` - Eliminar usuario (soft delete)

#### 3. Pacientes (`/patients`) - Doctor

- `GET /patients` - Listar pacientes del doctor
- `GET /patients/<id>` - Obtener paciente por ID
- `POST /patients` - Crear paciente
- `PUT /patients/<id>` - Actualizar paciente
- `DELETE /patients/<id>` - Eliminar paciente

#### 4. Historias Clínicas (`/medical-records`) - Doctor

- `GET /medical-records/patient/<id>` - Historias de un paciente
- `GET /medical-records/<id>` - Obtener historia por ID
- `POST /medical-records` - Crear historia clínica
- `GET /medical-records/mine` - Mis historias (paciente)

#### 5. Auditoría (`/audit`) - Solo Admin

- `GET /audit` - Listar logs de auditoría
- `GET /audit/user/<id>` - Logs de un usuario específico
- `GET /audit/stats` - Estadísticas de auditoría

#### 6. Criptografía (`/crypto`) - Demo Educativa

- `POST /crypto/aes/encrypt` - Demo cifrado AES
- `POST /crypto/aes/decrypt` - Demo descifrado AES
- `POST /crypto/rsa/generate` - Generar par de claves RSA
- `POST /crypto/rsa/encrypt` - Demo cifrado RSA
- `POST /crypto/rsa/decrypt` - Demo descifrado RSA
- `POST /crypto/hash/sha256` - Demo hash SHA-256
- `POST /crypto/hash/verify` - Verificar hash
- `POST /crypto/password/hash` - Demo hash bcrypt
- `POST /crypto/password/verify` - Verificar contraseña
- `POST /crypto/classic/caesar` - Cifrado César
- `POST /crypto/classic/vigenere` - Cifrado Vigenère

## 🧪 Ejemplos de Uso

### 1. Registro de Usuario

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor1",
    "password": "Doctor123!",
    "email": "doctor1@espe.edu.ec",
    "nombre": "Juan",
    "apellido": "Pérez",
    "cedula": "1234567890",
    "rol": "doctor"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor1",
    "password": "Doctor123!"
  }'
```

Respuesta:
```json
{
  "success": true,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "doctor1",
      "rol": "doctor",
      "nombre_completo": "Juan Pérez"
    }
  }
}
```

### 3. Crear Paciente

```bash
curl -X POST http://localhost:5000/api/v1/patients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "cedula": "0987654321",
    "nombre": "María",
    "apellido": "García",
    "fecha_nacimiento": "1990-05-15",
    "genero": "F",
    "telefono": "0987654321",
    "email": "maria.garcia@email.com",
    "alergias": "Penicilina",
    "antecedentes": "Hipertensión arterial"
  }'
```

### 4. Crear Historia Clínica

```bash
curl -X POST http://localhost:5000/api/v1/medical-records \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "paciente_id": 1,
    "fecha_consulta": "2024-01-15",
    "sintomas": "Fiebre, dolor de garganta",
    "diagnostico": "Faringitis aguda",
    "tratamiento": "Ibuprofeno 400mg cada 8 horas",
    "notas": "Control en 5 días",
    "recetas": [
      {
        "medicamento": "Ibuprofeno",
        "dosis": "400mg",
        "duracion_dias": 5,
        "instrucciones": "Tomar con alimentos"
      }
    ]
  }'
```

### 5. Demo Cifrado AES

```bash
curl -X POST http://localhost:5000/api/v1/crypto/aes/encrypt \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "plaintext": "Historia clínica confidencial"
  }'
```

## 🔒 Roles y Permisos

### Admin
- Gestionar usuarios (doctores)
- Ver logs de auditoría
- Acceso completo al sistema

### Doctor
- Gestionar pacientes
- Crear y ver historias clínicas
- Cifrar datos médicos

### Paciente
- Ver sus propias historias clínicas (solo lectura)
- Acceso limitado

## 🧪 Testing

### Ejecutar Tests

```bash
# Instalar dependencias de testing
pip install pytest pytest-flask pytest-cov

# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=. --cov-report=html

# Ver reporte de cobertura
# Se genera en htmlcov/index.html
```

### Estructura de Tests

```
tests/
├── test_crypto_service.py    # Tests de criptografía
├── test_auth.py               # Tests de autenticación
├── test_users.py              # Tests de usuarios
├── test_patients.py           # Tests de pacientes
└── test_medical_records.py   # Tests de historias clínicas
```

## 🔧 Troubleshooting

### Error: No module named 'psycopg2'

```bash
pip install psycopg2-binary
```

### Error: Could not connect to database

Verificar:
1. PostgreSQL está corriendo
2. Credenciales en `.env` son correctas
3. Base de datos existe

```bash
# Ver estado de PostgreSQL (Linux)
sudo systemctl status postgresql

# Iniciar PostgreSQL
sudo systemctl start postgresql
```

### Error: Invalid JWT token

- Token expiró (duración: 30 minutos)
- Volver a hacer login para obtener nuevo token

### Error: Permission denied

- Verificar que el usuario tiene el rol correcto
- Los doctores no pueden acceder a endpoints de admin

## 📊 Monitoreo y Logs

### Ver Logs de la Aplicación

```bash
# Los logs se muestran en la consola por defecto
# En producción, redirigir a archivo:
python app.py > logs/app.log 2>&1
```

### Consultar Logs de Auditoría

```bash
curl -X GET "http://localhost:5000/api/v1/audit?page=1&limit=20" \
  -H "Authorization: Bearer <admin_token>"
```

## 🚀 Deployment (Producción)

### Con Gunicorn y Nginx

1. Instalar Gunicorn:
```bash
pip install gunicorn
```

2. Ejecutar con Gunicorn:
```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

3. Configurar Nginx como reverse proxy:

```nginx
server {
    listen 80;
    server_name api.espe-medsafe.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Variables de Entorno de Producción

```env
FLASK_ENV=production
DEBUG=False
SQLALCHEMY_ECHO=False
```

### Consideraciones de Seguridad

1. Usar HTTPS en producción
2. Configurar CORS apropiadamente
3. Usar contraseñas fuertes para DB
4. Rotar JWT_SECRET_KEY periódicamente
5. Limitar intentos de login
6. Implementar rate limiting

## 📝 Licencia

Proyecto académico - Universidad de las Fuerzas Armadas ESPE
Materia: Ingeniería de Seguridad de Software
Docente: PhD. Walter Fuertes

## 👥 Autor

Desarrollado como parte del Proyecto Final - Parcial 3

---

**Nota**: Este es un proyecto educativo. Para uso en producción, implementar medidas de seguridad adicionales según estándares de la industria.
