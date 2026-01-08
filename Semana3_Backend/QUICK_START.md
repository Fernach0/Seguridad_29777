# 🚀 Guía Rápida - ESPE MedSafe Backend

## Inicio Rápido (5 minutos)

### 1. Instalación

```bash
# Clonar o navegar al proyecto
cd Semana3_Backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Base de Datos

```bash
# Crear base de datos PostgreSQL
createdb espe_medsafe
```

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Generar clave AES
python generate_key.py
```

Copiar la clave generada al archivo `.env` en `AES_MASTER_KEY`

### 4. Inicializar Base de Datos

```bash
python init_db.py
```

### 5. Ejecutar Aplicación

```bash
python app.py
```

La API estará en: http://localhost:5000

---

## 🔑 Credenciales por Defecto

```
Username: admin
Password: Admin123!
```

⚠️ **Cambiar después del primer login**

---

## 📡 Endpoints Principales

### Autenticación
```bash
# Login
POST http://localhost:5000/api/v1/auth/login
Body: {"username": "admin", "password": "Admin123!"}

# Obtener perfil
GET http://localhost:5000/api/v1/auth/me
Header: Authorization: Bearer <token>
```

### Usuarios (Admin)
```bash
# Crear doctor
POST http://localhost:5000/api/v1/users
Header: Authorization: Bearer <token>
Body: {
  "username": "doctor1",
  "password": "Doctor123!",
  "email": "doctor1@espe.edu.ec",
  "nombre": "Juan",
  "apellido": "Pérez",
  "cedula": "1234567890",
  "rol": "doctor"
}

# Listar usuarios
GET http://localhost:5000/api/v1/users
```

### Pacientes (Doctor)
```bash
# Crear paciente
POST http://localhost:5000/api/v1/patients
Body: {
  "cedula": "0987654321",
  "nombre": "María",
  "apellido": "García",
  "fecha_nacimiento": "1990-05-15",
  "alergias": "Penicilina",
  "antecedentes": "Hipertensión"
}

# Listar pacientes
GET http://localhost:5000/api/v1/patients
```

### Historias Clínicas (Doctor)
```bash
# Crear historia
POST http://localhost:5000/api/v1/medical-records
Body: {
  "paciente_id": 1,
  "fecha_consulta": "2024-01-15",
  "sintomas": "Fiebre, dolor de garganta",
  "diagnostico": "Faringitis aguda",
  "tratamiento": "Ibuprofeno 400mg cada 8 horas"
}

# Ver historias de paciente
GET http://localhost:5000/api/v1/medical-records/patient/1
```

### Demos Criptográficas
```bash
# Cifrar con AES
POST http://localhost:5000/api/v1/crypto/aes/encrypt
Body: {"plaintext": "Datos confidenciales"}

# Generar claves RSA
POST http://localhost:5000/api/v1/crypto/rsa/generate

# Hash SHA-256
POST http://localhost:5000/api/v1/crypto/hash/sha256
Body: {"data": "Historia clínica"}

# Cifrado César
POST http://localhost:5000/api/v1/crypto/classic/caesar
Body: {"text": "HOLA", "shift": 3, "encrypt": true}
```

---

## 🧪 Testing con cURL

### 1. Login y obtener token

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"Admin123!\"}"
```

Guardar el token de la respuesta.

### 2. Crear doctor

```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d "{\"username\":\"doctor1\",\"password\":\"Doctor123!\",\"email\":\"doctor1@espe.edu.ec\",\"nombre\":\"Juan\",\"apellido\":\"Pérez\",\"cedula\":\"1234567890\",\"rol\":\"doctor\"}"
```

### 3. Login como doctor

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"doctor1\",\"password\":\"Doctor123!\"}"
```

### 4. Crear paciente

```bash
curl -X POST http://localhost:5000/api/v1/patients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN_DEL_DOCTOR" \
  -d "{\"cedula\":\"0987654321\",\"nombre\":\"María\",\"apellido\":\"García\",\"fecha_nacimiento\":\"1990-05-15\",\"alergias\":\"Penicilina\"}"
```

---

## 🔧 Comandos Útiles

### Ver logs de auditoría

```bash
curl -X GET "http://localhost:5000/api/v1/audit?page=1" \
  -H "Authorization: Bearer TOKEN_ADMIN"
```

### Ver estadísticas

```bash
curl -X GET http://localhost:5000/api/v1/audit/stats \
  -H "Authorization: Bearer TOKEN_ADMIN"
```

### Health check

```bash
curl http://localhost:5000/health
```

---

## 📝 Notas Importantes

1. **Tokens JWT**: Expiran en 30 minutos
2. **Roles**: admin (gestiona usuarios), doctor (gestiona pacientes), paciente (solo lectura)
3. **Cifrado**: Alergias, antecedentes e historias clínicas se cifran automáticamente
4. **Auditoría**: Todas las acciones importantes se registran
5. **Integridad**: SHA-256 verifica que las historias no se modifiquen

---

## 🐛 Troubleshooting

### Error de conexión a DB
```bash
# Verificar que PostgreSQL está corriendo
# Windows:
pg_ctl status

# Verificar credenciales en .env
```

### Token inválido
```bash
# El token expiró, hacer login nuevamente
```

### Error al cifrar
```bash
# Verificar que AES_MASTER_KEY está configurada
python generate_key.py
# Copiar al .env
```

---

## 📚 Documentación Completa

Ver `README.md` para documentación detallada.

---

## 🎯 Siguiente Paso: Semana 4

Frontend con React conectándose a estos endpoints.
