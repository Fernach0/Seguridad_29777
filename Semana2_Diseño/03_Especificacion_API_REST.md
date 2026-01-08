# ESPECIFICACIÓN DE API REST
## ESPE MedSafe - Semana 2

---

## 1. INFORMACIÓN GENERAL DE LA API

### 1.1 Base URL
```
http://localhost:5000/api/v1
```

### 1.2 Formato de Respuesta
Todas las respuestas están en formato **JSON**.

### 1.3 Autenticación
- **Método**: JWT (JSON Web Token)
- **Header requerido**: `Authorization: Bearer <token>`
- **Expiración**: 30 minutos

### 1.4 Códigos de Estado HTTP

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado exitosamente |
| 400 | Bad Request | Datos de entrada inválidos |
| 401 | Unauthorized | Token inválido o expirado |
| 403 | Forbidden | Sin permisos para esta acción |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | Conflicto (ej: usuario ya existe) |
| 500 | Internal Server Error | Error del servidor |

---

## 2. DIAGRAMA DE ENDPOINTS

```mermaid
graph TB
    subgraph "🔐 Autenticación"
        AUTH1[POST /auth/login]
        AUTH2[POST /auth/logout]
        AUTH3[POST /auth/refresh]
        AUTH4[GET /auth/me]
    end
    
    subgraph "👥 Usuarios (Admin)"
        USER1[POST /users]
        USER2[GET /users]
        USER3[GET /users/:id]
        USER4[PUT /users/:id]
        USER5[DELETE /users/:id]
    end
    
    subgraph "🧑‍⚕️ Pacientes (Doctor)"
        PAT1[POST /patients]
        PAT2[GET /patients]
        PAT3[GET /patients/:id]
        PAT4[PUT /patients/:id]
        PAT5[DELETE /patients/:id]
    end
    
    subgraph "📋 Historias Clínicas"
        HC1[POST /medical-records]
        HC2[GET /medical-records/patient/:id]
        HC3[GET /medical-records/:id]
        HC4[PUT /medical-records/:id]
        HC5[GET /medical-records/mine]
    end
    
    subgraph "💊 Recetas"
        REC1[POST /prescriptions]
        REC2[GET /prescriptions/medical-record/:id]
        REC3[GET /prescriptions/:id]
    end
    
    subgraph "📊 Auditoría (Admin)"
        AUD1[GET /audit-logs]
        AUD2[GET /audit-logs/user/:id]
    end
    
    subgraph "🔒 Criptografía (Demo)"
        CRY1[POST /crypto/encrypt]
        CRY2[POST /crypto/decrypt]
        CRY3[POST /crypto/hash]
        CRY4[POST /crypto/classic/caesar]
        CRY5[POST /crypto/classic/vigenere]
    end
    
    style AUTH1 fill:#f8d7da
    style USER1 fill:#cce5ff
    style PAT1 fill:#fff3cd
    style HC1 fill:#d4edda
    style REC1 fill:#ffe6e6
    style AUD1 fill:#d1ecf1
    style CRY1 fill:#e2e3e5
```

---

## 3. ENDPOINTS DETALLADOS

### 3.1 AUTENTICACIÓN

#### 3.1.1 Login

```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "username": "doctor1",
  "password": "Doctor123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 2,
      "username": "doctor1",
      "rol": "doctor",
      "nombre": "Juan",
      "apellido": "Pérez",
      "email": "juan.perez@espe.edu.ec"
    }
  },
  "message": "Login exitoso"
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Credenciales inválidas"
}
```

---

#### 3.1.2 Logout

```http
POST /api/v1/auth/logout
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

---

#### 3.1.3 Refresh Token

```http
POST /api/v1/auth/refresh
```

**Headers:**
```
Authorization: Bearer <token_expired>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

#### 3.1.4 Usuario Actual

```http
GET /api/v1/auth/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "username": "doctor1",
    "rol": "doctor",
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@espe.edu.ec",
    "activo": true
  }
}
```

---

### 3.2 USUARIOS (Solo Administrador)

#### 3.2.1 Crear Usuario (Doctor)

```http
POST /api/v1/users
```

**Permisos requeridos:** Administrador

**Request Body:**
```json
{
  "username": "doctor2",
  "password": "Doctor123!",
  "rol": "doctor",
  "nombre": "María",
  "apellido": "López",
  "email": "maria.lopez@espe.edu.ec",
  "cedula": "1234567891"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "username": "doctor2",
    "rol": "doctor",
    "nombre": "María",
    "apellido": "López",
    "email": "maria.lopez@espe.edu.ec",
    "cedula": "1234567891",
    "activo": true,
    "created_at": "2026-01-08T10:30:00Z"
  },
  "message": "Usuario creado exitosamente"
}
```

**Response (409 Conflict):**
```json
{
  "success": false,
  "error": "El username ya existe"
}
```

---

#### 3.2.2 Listar Usuarios

```http
GET /api/v1/users?rol=doctor&activo=true&page=1&limit=10
```

**Query Parameters:**
- `rol` (opcional): admin | doctor | paciente
- `activo` (opcional): true | false
- `page` (opcional, default: 1): Número de página
- `limit` (opcional, default: 10): Registros por página

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "users": [
      {
        "id": 2,
        "username": "doctor1",
        "rol": "doctor",
        "nombre": "Juan",
        "apellido": "Pérez",
        "email": "juan.perez@espe.edu.ec",
        "activo": true
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

---

#### 3.2.3 Obtener Usuario por ID

```http
GET /api/v1/users/2
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "username": "doctor1",
    "rol": "doctor",
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@espe.edu.ec",
    "cedula": "0987654321",
    "activo": true,
    "created_at": "2026-01-01T08:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  }
}
```

---

#### 3.2.4 Actualizar Usuario

```http
PUT /api/v1/users/2
```

**Request Body:**
```json
{
  "nombre": "Juan Carlos",
  "apellido": "Pérez García",
  "email": "juan.perez.garcia@espe.edu.ec",
  "activo": true
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 2,
    "username": "doctor1",
    "nombre": "Juan Carlos",
    "apellido": "Pérez García",
    "email": "juan.perez.garcia@espe.edu.ec",
    "activo": true
  },
  "message": "Usuario actualizado exitosamente"
}
```

---

#### 3.2.5 Eliminar Usuario (Desactivar)

```http
DELETE /api/v1/users/2
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Usuario desactivado exitosamente"
}
```

---

### 3.3 PACIENTES (Doctor)

#### 3.3.1 Crear Paciente

```http
POST /api/v1/patients
```

**Permisos requeridos:** Doctor

**Request Body:**
```json
{
  "cedula": "1723456789",
  "nombre": "Carlos",
  "apellido": "Ramírez",
  "fecha_nacimiento": "1985-03-20",
  "genero": "M",
  "telefono": "0998765432",
  "email": "carlos.ramirez@email.com",
  "direccion": "Av. Occidental N45-234 y Gaspar de Carvajal",
  "grupo_sanguineo": "A+",
  "alergias": "Penicilina, Mariscos",
  "antecedentes": "Diabetes tipo 2, Hipertensión"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 15,
    "cedula": "1723456789",
    "nombre": "Carlos",
    "apellido": "Ramírez",
    "fecha_nacimiento": "1985-03-20",
    "genero": "M",
    "telefono": "0998765432",
    "email": "carlos.ramirez@email.com",
    "grupo_sanguineo": "A+",
    "doctor_id": 2,
    "created_at": "2026-01-08T11:00:00Z"
  },
  "message": "Paciente creado exitosamente"
}
```

**Nota:** Los campos `alergias` y `antecedentes` se cifran automáticamente con AES-256.

---

#### 3.3.2 Listar Pacientes

```http
GET /api/v1/patients?search=Carlos&page=1&limit=10
```

**Query Parameters:**
- `search` (opcional): Busca en nombre, apellido o cédula
- `page` (opcional, default: 1)
- `limit` (opcional, default: 10)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": 15,
        "cedula": "1723456789",
        "nombre": "Carlos",
        "apellido": "Ramírez",
        "fecha_nacimiento": "1985-03-20",
        "genero": "M",
        "telefono": "0998765432",
        "grupo_sanguineo": "A+",
        "edad": 40
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 45,
      "pages": 5
    }
  }
}
```

---

#### 3.3.3 Obtener Paciente por ID

```http
GET /api/v1/patients/15
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 15,
    "cedula": "1723456789",
    "nombre": "Carlos",
    "apellido": "Ramírez",
    "fecha_nacimiento": "1985-03-20",
    "genero": "M",
    "telefono": "0998765432",
    "email": "carlos.ramirez@email.com",
    "direccion": "Av. Occidental N45-234 y Gaspar de Carvajal",
    "grupo_sanguineo": "A+",
    "alergias": "Penicilina, Mariscos",
    "antecedentes": "Diabetes tipo 2, Hipertensión",
    "doctor_id": 2,
    "created_at": "2026-01-08T11:00:00Z"
  }
}
```

**Nota:** Los campos cifrados se descifran automáticamente antes de enviar.

---

#### 3.3.4 Actualizar Paciente

```http
PUT /api/v1/patients/15
```

**Request Body:**
```json
{
  "telefono": "0999888777",
  "email": "carlos.ramirez.nuevo@email.com",
  "direccion": "Nueva dirección actualizada"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 15,
    "telefono": "0999888777",
    "email": "carlos.ramirez.nuevo@email.com",
    "direccion": "Nueva dirección actualizada"
  },
  "message": "Paciente actualizado exitosamente"
}
```

---

#### 3.3.5 Eliminar Paciente

```http
DELETE /api/v1/patients/15
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Paciente eliminado exitosamente"
}
```

---

### 3.4 HISTORIAS CLÍNICAS

#### 3.4.1 Crear Historia Clínica

```http
POST /api/v1/medical-records
```

**Permisos requeridos:** Doctor

**Request Body:**
```json
{
  "paciente_id": 15,
  "fecha_consulta": "2026-01-08",
  "sintomas": "Fiebre alta (39°C), tos seca, dolor de garganta",
  "diagnostico": "Faringitis aguda bacteriana",
  "tratamiento": "Reposo, hidratación abundante, analgésicos",
  "notas": "Paciente presenta cuadro de 3 días de evolución",
  "recetas": [
    {
      "medicamento": "Amoxicilina 500mg",
      "dosis": "1 cápsula cada 8 horas",
      "duracion_dias": 7,
      "instrucciones": "Tomar con alimentos"
    },
    {
      "medicamento": "Paracetamol 500mg",
      "dosis": "1 tableta cada 6 horas",
      "duracion_dias": 3,
      "instrucciones": "Solo si hay fiebre o dolor"
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 234,
    "paciente_id": 15,
    "doctor_id": 2,
    "fecha_consulta": "2026-01-08",
    "hash_integridad": "a3f5c8d9e2b1...",
    "created_at": "2026-01-08T11:30:00Z"
  },
  "message": "Historia clínica creada exitosamente"
}
```

**Nota:** Los campos `sintomas`, `diagnostico`, `tratamiento` y `notas` se cifran con AES-256 antes de almacenar.

---

#### 3.4.2 Obtener Historias de un Paciente

```http
GET /api/v1/medical-records/patient/15
```

**Permisos requeridos:** Doctor (propietario) o Paciente (solo sus propias historias)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "paciente": {
      "id": 15,
      "nombre": "Carlos",
      "apellido": "Ramírez",
      "cedula": "1723456789"
    },
    "historias": [
      {
        "id": 234,
        "fecha_consulta": "2026-01-08",
        "doctor": "Dr. Juan Pérez",
        "sintomas": "Fiebre alta (39°C), tos seca, dolor de garganta",
        "diagnostico": "Faringitis aguda bacteriana",
        "tratamiento": "Reposo, hidratación abundante, analgésicos",
        "integridad_verificada": true
      },
      {
        "id": 220,
        "fecha_consulta": "2025-12-15",
        "doctor": "Dr. Juan Pérez",
        "sintomas": "Dolor abdominal, náuseas",
        "diagnostico": "Gastritis aguda",
        "tratamiento": "Omeprazol 20mg por 14 días",
        "integridad_verificada": true
      }
    ]
  }
}
```

---

#### 3.4.3 Obtener Historia Clínica por ID

```http
GET /api/v1/medical-records/234
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 234,
    "paciente": {
      "id": 15,
      "nombre": "Carlos Ramírez",
      "cedula": "1723456789"
    },
    "doctor": {
      "id": 2,
      "nombre": "Dr. Juan Pérez"
    },
    "fecha_consulta": "2026-01-08",
    "sintomas": "Fiebre alta (39°C), tos seca, dolor de garganta",
    "diagnostico": "Faringitis aguda bacteriana",
    "tratamiento": "Reposo, hidratación abundante, analgésicos",
    "notas": "Paciente presenta cuadro de 3 días de evolución",
    "integridad_verificada": true,
    "created_at": "2026-01-08T11:30:00Z"
  }
}
```

---

#### 3.4.4 Actualizar Historia Clínica

```http
PUT /api/v1/medical-records/234
```

**Request Body:**
```json
{
  "tratamiento": "Reposo, hidratación abundante, analgésicos. Actualización: Se agrega antiinflamatorio",
  "notas": "Paciente presenta mejoría después de 2 días de tratamiento"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 234,
    "tratamiento": "Reposo, hidratación abundante, analgésicos. Actualización: Se agrega antiinflamatorio",
    "notas": "Paciente presenta mejoría después de 2 días de tratamiento",
    "hash_integridad": "b4e6d9f3a2c8...",
    "updated_at": "2026-01-10T09:15:00Z"
  },
  "message": "Historia clínica actualizada exitosamente"
}
```

---

#### 3.4.5 Obtener Mis Historias (Paciente)

```http
GET /api/v1/medical-records/mine
```

**Permisos requeridos:** Paciente (token JWT con rol "paciente")

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "historias": [
      {
        "id": 234,
        "fecha_consulta": "2026-01-08",
        "doctor": "Dr. Juan Pérez",
        "sintomas": "Fiebre alta (39°C), tos seca, dolor de garganta",
        "diagnostico": "Faringitis aguda bacteriana",
        "tratamiento": "Reposo, hidratación abundante, analgésicos"
      }
    ]
  }
}
```

---

### 3.5 RECETAS

#### 3.5.1 Crear Receta

```http
POST /api/v1/prescriptions
```

**Request Body:**
```json
{
  "historia_clinica_id": 234,
  "medicamento": "Ibuprofeno 400mg",
  "dosis": "1 tableta cada 8 horas",
  "duracion_dias": 5,
  "instrucciones": "Tomar después de las comidas"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": 456,
    "historia_clinica_id": 234,
    "medicamento": "Ibuprofeno 400mg",
    "dosis": "1 tableta cada 8 horas",
    "duracion_dias": 5,
    "instrucciones": "Tomar después de las comidas",
    "created_at": "2026-01-08T11:35:00Z"
  },
  "message": "Receta creada exitosamente"
}
```

---

#### 3.5.2 Obtener Recetas de una Historia Clínica

```http
GET /api/v1/prescriptions/medical-record/234
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "recetas": [
      {
        "id": 455,
        "medicamento": "Amoxicilina 500mg",
        "dosis": "1 cápsula cada 8 horas",
        "duracion_dias": 7,
        "instrucciones": "Tomar con alimentos"
      },
      {
        "id": 456,
        "medicamento": "Ibuprofeno 400mg",
        "dosis": "1 tableta cada 8 horas",
        "duracion_dias": 5,
        "instrucciones": "Tomar después de las comidas"
      }
    ]
  }
}
```

---

### 3.6 AUDITORÍA (Administrador)

#### 3.6.1 Obtener Logs de Auditoría

```http
GET /api/v1/audit-logs?accion=LOGIN&fecha_desde=2026-01-01&fecha_hasta=2026-01-08&page=1&limit=50
```

**Query Parameters:**
- `accion` (opcional): LOGIN | LOGOUT | CREATE | UPDATE | DELETE | VIEW
- `usuario_id` (opcional): ID del usuario
- `tabla_afectada` (opcional): usuarios | pacientes | historias_clinicas
- `fecha_desde` (opcional): YYYY-MM-DD
- `fecha_hasta` (opcional): YYYY-MM-DD
- `page` (opcional, default: 1)
- `limit` (opcional, default: 50)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "logs": [
      {
        "id": 1523,
        "usuario": "doctor1 (Juan Pérez)",
        "accion": "LOGIN",
        "ip_address": "192.168.1.105",
        "timestamp": "2026-01-08T09:15:30Z"
      },
      {
        "id": 1524,
        "usuario": "doctor1 (Juan Pérez)",
        "accion": "CREATE",
        "tabla_afectada": "historias_clinicas",
        "registro_id": 234,
        "ip_address": "192.168.1.105",
        "timestamp": "2026-01-08T11:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 50,
      "total": 1523,
      "pages": 31
    }
  }
}
```

---

#### 3.6.2 Obtener Logs de un Usuario

```http
GET /api/v1/audit-logs/user/2
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "usuario": {
      "id": 2,
      "username": "doctor1",
      "nombre": "Juan Pérez"
    },
    "logs": [
      {
        "id": 1523,
        "accion": "LOGIN",
        "ip_address": "192.168.1.105",
        "timestamp": "2026-01-08T09:15:30Z"
      },
      {
        "id": 1524,
        "accion": "CREATE",
        "tabla_afectada": "historias_clinicas",
        "timestamp": "2026-01-08T11:30:00Z"
      }
    ]
  }
}
```

---

### 3.7 CRIPTOGRAFÍA (Módulo Educativo/Demo)

#### 3.7.1 Cifrar con AES

```http
POST /api/v1/crypto/encrypt
```

**Request Body:**
```json
{
  "text": "Este es un mensaje secreto",
  "algorithm": "AES-256"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "original": "Este es un mensaje secreto",
    "encrypted": "8f3c5a9b2d...",
    "iv": "a1b2c3d4e5f6...",
    "algorithm": "AES-256-CBC"
  }
}
```

---

#### 3.7.2 Descifrar con AES

```http
POST /api/v1/crypto/decrypt
```

**Request Body:**
```json
{
  "encrypted": "8f3c5a9b2d...",
  "iv": "a1b2c3d4e5f6...",
  "algorithm": "AES-256"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "decrypted": "Este es un mensaje secreto",
    "algorithm": "AES-256-CBC"
  }
}
```

---

#### 3.7.3 Calcular Hash

```http
POST /api/v1/crypto/hash
```

**Request Body:**
```json
{
  "text": "Este es un mensaje para hashear",
  "algorithm": "SHA-256"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "original": "Este es un mensaje para hashear",
    "hash": "a3f5c8d9e2b1f4a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
    "algorithm": "SHA-256"
  }
}
```

---

#### 3.7.4 Cifrado César

```http
POST /api/v1/crypto/classic/caesar
```

**Request Body:**
```json
{
  "text": "HOLA MUNDO",
  "shift": 3,
  "operation": "encrypt"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "original": "HOLA MUNDO",
    "result": "KROD PXQGR",
    "shift": 3,
    "operation": "encrypt"
  }
}
```

---

#### 3.7.5 Cifrado Vigenère

```http
POST /api/v1/crypto/classic/vigenere
```

**Request Body:**
```json
{
  "text": "MEDICINA",
  "key": "ESPE",
  "operation": "encrypt"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "original": "MEDICINA",
    "result": "QIHMMRME",
    "key": "ESPE",
    "operation": "encrypt"
  }
}
```

---

## 4. ESTRUCTURA DE RESPUESTA ESTÁNDAR

### 4.1 Respuesta Exitosa

```json
{
  "success": true,
  "data": { ... },
  "message": "Mensaje descriptivo opcional"
}
```

### 4.2 Respuesta con Error

```json
{
  "success": false,
  "error": "Descripción del error",
  "details": {
    "field": "password",
    "reason": "La contraseña debe tener al menos 8 caracteres"
  }
}
```

---

## 5. AUTENTICACIÓN CON JWT

### 5.1 Payload del Token

```json
{
  "user_id": 2,
  "username": "doctor1",
  "rol": "doctor",
  "iat": 1704710400,
  "exp": 1704712200
}
```

### 5.2 Uso del Token

```http
GET /api/v1/patients
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImRvY3RvcjEiLCJyb2wiOiJkb2N0b3IiLCJpYXQiOjE3MDQ3MTA0MDAsImV4cCI6MTcwNDcxMjIwMH0.abcd1234...
```

---

## 6. CONTROL DE ACCESO BASADO EN ROLES

| Endpoint | Admin | Doctor | Paciente |
|----------|-------|--------|----------|
| POST /users | ✅ | ❌ | ❌ |
| GET /users | ✅ | ❌ | ❌ |
| POST /patients | ❌ | ✅ | ❌ |
| GET /patients/:id | ❌ | ✅ | ❌ |
| POST /medical-records | ❌ | ✅ | ❌ |
| GET /medical-records/mine | ❌ | ❌ | ✅ |
| GET /audit-logs | ✅ | ❌ | ❌ |
| POST /crypto/* | ✅ | ✅ | ✅ |

---

## 7. VALIDACIONES

### 7.1 Usuario
- `username`: 4-50 caracteres, alfanumérico
- `password`: Mínimo 8 caracteres, incluir mayúscula, minúscula, número, símbolo
- `email`: Formato válido de email
- `cedula`: Exactamente 10 dígitos

### 7.2 Paciente
- `cedula`: Exactamente 10 dígitos, único
- `fecha_nacimiento`: No puede ser futura
- `telefono`: 10 dígitos (opcional)
- `email`: Formato válido (opcional)

### 7.3 Historia Clínica
- `paciente_id`: Debe existir
- `fecha_consulta`: No puede ser futura
- `sintomas`: Mínimo 10 caracteres
- `diagnostico`: Mínimo 10 caracteres

---

## 8. RATIOS Y THROTTLING

- **Rate Limit**: 100 requests por minuto por IP
- **Login Attempts**: Máximo 5 intentos fallidos en 15 minutos
- **Token Expiration**: 30 minutos
- **Refresh Token Expiration**: 7 días

---

**Fecha**: 8 de enero de 2026  
**Equipo**: ESPE MedSafe  
**Semana**: 2 - Especificación de API REST
