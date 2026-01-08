# ARQUITECTURA DEL SISTEMA
## ESPE MedSafe - Semana 2

---

## 1. ARQUITECTURA GENERAL DEL SISTEMA

### 1.1 Vista de Alto Nivel

```mermaid
graph TB
    subgraph "Capa de Presentación"
        UI[🖥️ Interfaz Web<br/>HTML/CSS/JavaScript]
    end
    
    subgraph "Capa de Aplicación"
        API[⚙️ API REST<br/>Flask/FastAPI]
        AUTH[🔐 Módulo de Autenticación<br/>JWT/Session]
        CRYPTO[🔒 Módulo Criptográfico<br/>AES/RSA/bcrypt]
        AUDIT[📋 Módulo de Auditoría<br/>Logs]
    end
    
    subgraph "Capa de Datos"
        DB[(💾 Base de Datos<br/>PostgreSQL/MySQL)]
        CACHE[(⚡ Cache<br/>Redis - Opcional)]
    end
    
    UI -->|HTTPS| API
    API --> AUTH
    API --> CRYPTO
    API --> AUDIT
    API --> DB
    AUTH --> DB
    AUDIT --> DB
    CRYPTO --> DB
    API -.->|Opcional| CACHE
    
    style UI fill:#e1f5ff
    style API fill:#fff3cd
    style AUTH fill:#f8d7da
    style CRYPTO fill:#d4edda
    style AUDIT fill:#d1ecf1
    style DB fill:#e2e3e5
    style CACHE fill:#e7e8ea
```

### 1.2 Arquitectura Cliente-Servidor

```mermaid
sequenceDiagram
    participant U as 👤 Usuario<br/>(Navegador)
    participant F as 🖥️ Frontend<br/>(HTML/JS)
    participant N as 🌐 Nginx<br/>(Web Server)
    participant B as ⚙️ Backend<br/>(Flask API)
    participant C as 🔐 Crypto Module
    participant D as 💾 Database
    
    U->>F: Accede a la aplicación
    F->>N: Solicitud HTTPS
    N->>B: Reenvía a API
    B->>B: Valida sesión/token
    B->>C: Cifra/Descifra datos
    C->>B: Datos procesados
    B->>D: Query cifrado
    D->>B: Resultado cifrado
    B->>C: Descifra para enviar
    C->>B: Datos en claro
    B->>N: Respuesta JSON
    N->>F: Respuesta HTTPS
    F->>U: Muestra información
```

---

## 2. ARQUITECTURA DE CAPAS DETALLADA

### 2.1 Capa de Presentación (Frontend)

```mermaid
graph LR
    subgraph "Frontend Components"
        LOGIN[🔑 Login Page]
        DASH_ADMIN[👨‍💼 Dashboard Admin]
        DASH_DOCTOR[👨‍⚕️ Dashboard Doctor]
        DASH_PATIENT[🧑‍🦱 Dashboard Paciente]
        FORMS[📝 Formularios CRUD]
        VIEWS[👁️ Vistas de Consulta]
    end
    
    subgraph "Frontend Services"
        AUTH_S[Auth Service]
        API_S[API Service]
        CRYPTO_DEMO[Demo Cifrado Clásico]
    end
    
    LOGIN --> AUTH_S
    DASH_ADMIN --> API_S
    DASH_DOCTOR --> API_S
    DASH_PATIENT --> API_S
    FORMS --> API_S
    VIEWS --> API_S
    CRYPTO_DEMO --> API_S
    
    style LOGIN fill:#ffcccc
    style DASH_ADMIN fill:#cce5ff
    style DASH_DOCTOR fill:#d4edda
    style DASH_PATIENT fill:#fff3cd
```

**Componentes:**
- **Login Page**: Formulario de autenticación con validación
- **Dashboards**: Interfaces específicas por rol
- **Formularios CRUD**: Crear/editar pacientes e historias clínicas
- **Vistas de Consulta**: Lectura de datos
- **Demo Cifrado**: Módulo educativo interactivo

**Tecnologías:**
- HTML5, CSS3, JavaScript ES6+
- Bootstrap 5 o React (a definir)
- Axios o Fetch API para comunicación
- LocalStorage para tokens de sesión

---

### 2.2 Capa de Aplicación (Backend)

```mermaid
graph TB
    subgraph "API REST Layer"
        ROUTES[📍 Rutas/Endpoints]
        MIDDLEWARE[🛡️ Middleware<br/>Auth/CORS/Validation]
    end
    
    subgraph "Business Logic"
        AUTH_CTRL[🔐 Controlador Auth]
        USER_CTRL[👥 Controlador Usuarios]
        PATIENT_CTRL[🧑‍⚕️ Controlador Pacientes]
        HC_CTRL[📋 Controlador Historias Clínicas]
        AUDIT_CTRL[📊 Controlador Auditoría]
    end
    
    subgraph "Services Layer"
        CRYPTO_SVC[🔒 Servicio Criptográfico]
        AUTH_SVC[🎫 Servicio Autenticación]
        AUDIT_SVC[📝 Servicio Auditoría]
    end
    
    subgraph "Data Access Layer"
        MODELS[📦 Modelos ORM]
        DB_CONN[🔌 Database Connection]
    end
    
    ROUTES --> MIDDLEWARE
    MIDDLEWARE --> AUTH_CTRL
    MIDDLEWARE --> USER_CTRL
    MIDDLEWARE --> PATIENT_CTRL
    MIDDLEWARE --> HC_CTRL
    MIDDLEWARE --> AUDIT_CTRL
    
    AUTH_CTRL --> AUTH_SVC
    USER_CTRL --> CRYPTO_SVC
    PATIENT_CTRL --> CRYPTO_SVC
    HC_CTRL --> CRYPTO_SVC
    HC_CTRL --> AUDIT_SVC
    AUTH_CTRL --> AUDIT_SVC
    
    AUTH_SVC --> MODELS
    CRYPTO_SVC --> MODELS
    AUDIT_SVC --> MODELS
    MODELS --> DB_CONN
    
    style ROUTES fill:#fff3cd
    style MIDDLEWARE fill:#f8d7da
    style CRYPTO_SVC fill:#d4edda
    style AUTH_SVC fill:#cce5ff
    style AUDIT_SVC fill:#d1ecf1
```

**Estructura de Directorios Backend:**
```
backend/
├── app.py                    # Punto de entrada de la aplicación
├── config.py                 # Configuración (DB, claves, etc.)
├── requirements.txt          # Dependencias Python
├── routes/                   # Definición de rutas API
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── patient_routes.py
│   ├── medical_record_routes.py
│   └── audit_routes.py
├── controllers/              # Lógica de negocio
│   ├── auth_controller.py
│   ├── user_controller.py
│   ├── patient_controller.py
│   ├── medical_record_controller.py
│   └── audit_controller.py
├── services/                 # Servicios reutilizables
│   ├── crypto_service.py     # AES, RSA, SHA-256
│   ├── auth_service.py       # JWT, bcrypt
│   ├── audit_service.py      # Logging
│   └── classic_cipher.py     # César, Vigenère
├── models/                   # Modelos de base de datos (ORM)
│   ├── user.py
│   ├── patient.py
│   ├── medical_record.py
│   └── audit_log.py
├── middleware/               # Middleware personalizado
│   ├── auth_middleware.py
│   ├── role_middleware.py
│   └── validation_middleware.py
└── utils/                    # Utilidades
    ├── validators.py
    └── helpers.py
```

---

### 2.3 Capa de Datos

```mermaid
graph TB
    subgraph "Database Layer"
        USERS[(👥 Tabla Usuarios)]
        PATIENTS[(🧑‍⚕️ Tabla Pacientes)]
        RECORDS[(📋 Tabla Historias Clínicas)]
        AUDIT[(📊 Tabla Logs Auditoría)]
        KEYS[(🔑 Tabla Claves RSA)]
    end
    
    USERS -->|1:N| RECORDS
    PATIENTS -->|1:N| RECORDS
    USERS -->|1:N| AUDIT
    USERS -->|1:1| KEYS
    
    style USERS fill:#cce5ff
    style PATIENTS fill:#fff3cd
    style RECORDS fill:#d4edda
    style AUDIT fill:#d1ecf1
    style KEYS fill:#f8d7da
```

---

## 3. FLUJO DE DATOS CON CIFRADO

### 3.1 Flujo de Creación de Historia Clínica

```mermaid
sequenceDiagram
    participant D as 👨‍⚕️ Doctor
    participant F as Frontend
    participant API as Backend API
    participant CS as Crypto Service
    participant AS as Audit Service
    participant DB as Database
    
    D->>F: Redacta diagnóstico
    F->>API: POST /api/medical-records
    API->>API: Valida token JWT
    API->>API: Verifica rol (Doctor)
    API->>CS: Cifra diagnóstico (AES-256)
    CS->>CS: Genera IV aleatorio
    CS->>CS: Cifra con clave maestra
    CS-->>API: Datos cifrados + IV
    API->>CS: Calcula SHA-256 (integridad)
    CS-->>API: Hash SHA-256
    API->>DB: INSERT historia cifrada
    DB-->>API: ID de registro
    API->>AS: Registra acción en log
    AS->>DB: INSERT audit_log
    API-->>F: Respuesta exitosa
    F-->>D: Confirmación visual
```

### 3.2 Flujo de Consulta de Historia Clínica

```mermaid
sequenceDiagram
    participant P as 🧑‍🦱 Paciente
    participant F as Frontend
    participant API as Backend API
    participant CS as Crypto Service
    participant DB as Database
    
    P->>F: Solicita ver historial
    F->>API: GET /api/medical-records/mine
    API->>API: Valida token JWT
    API->>API: Verifica rol (Paciente)
    API->>DB: SELECT historias WHERE paciente_id = ?
    DB-->>API: Datos cifrados
    API->>CS: Descifra diagnóstico (AES-256)
    CS->>CS: Usa IV almacenado
    CS-->>API: Datos en claro
    API->>CS: Verifica hash SHA-256
    CS-->>API: Integridad OK/FAIL
    alt Integridad OK
        API-->>F: JSON con datos
        F-->>P: Muestra historial
    else Integridad Comprometida
        API-->>F: Error de integridad
        F-->>P: Alerta de seguridad
    end
```

### 3.3 Flujo de Autenticación con bcrypt

```mermaid
sequenceDiagram
    participant U as 👤 Usuario
    participant F as Frontend
    participant API as Backend API
    participant AUTH as Auth Service
    participant DB as Database
    
    U->>F: Ingresa usuario/password
    F->>API: POST /api/auth/login
    API->>DB: SELECT user WHERE username = ?
    DB-->>API: user {id, username, password_hash, salt, role}
    API->>AUTH: Verifica password con bcrypt
    AUTH->>AUTH: bcrypt.checkpw(password, hash)
    
    alt Password Correcto
        AUTH-->>API: ✅ Autenticación exitosa
        API->>API: Genera JWT con payload {id, role}
        API-->>F: Token JWT
        F->>F: Guarda token en localStorage
        F-->>U: Redirige a dashboard
    else Password Incorrecto
        AUTH-->>API: ❌ Autenticación fallida
        API-->>F: Error 401
        F-->>U: Mensaje de error genérico
    end
```

---

## 4. SEGURIDAD EN LA ARQUITECTURA

### 4.1 Capas de Seguridad

```mermaid
graph TB
    subgraph "Nivel 1: Transporte"
        HTTPS[🔒 HTTPS/TLS 1.3]
    end
    
    subgraph "Nivel 2: Autenticación"
        JWT[🎫 JWT Token]
        SESSION[🔐 Session Management]
    end
    
    subgraph "Nivel 3: Autorización"
        RBAC[👮 Role-Based Access Control]
        PERMS[✅ Validación de Permisos]
    end
    
    subgraph "Nivel 4: Datos"
        AES[🔐 AES-256 Cifrado]
        RSA[🔑 RSA-2048 Firma]
        BCRYPT[🔒 bcrypt Password Hash]
    end
    
    subgraph "Nivel 5: Infraestructura"
        FIREWALL[🛡️ Firewall]
        SELINUX[⚔️ SELinux]
        SSH[🔐 OpenSSH]
    end
    
    HTTPS --> JWT
    JWT --> RBAC
    RBAC --> AES
    AES --> FIREWALL
    
    style HTTPS fill:#d4edda
    style JWT fill:#cce5ff
    style RBAC fill:#fff3cd
    style AES fill:#f8d7da
    style FIREWALL fill:#e2e3e5
```

### 4.2 Protecciones Implementadas

| Amenaza | Protección | Capa |
|---------|-----------|------|
| Man-in-the-Middle | HTTPS/TLS | Transporte |
| Robo de sesión | JWT con expiración (30 min) | Autenticación |
| Acceso no autorizado | RBAC + Middleware | Autorización |
| SQL Injection | ORM + Queries parametrizadas | Datos |
| XSS | Validación + Escapado | Presentación |
| CSRF | CSRF Tokens | Presentación |
| Fuerza bruta | Rate limiting + bcrypt lento | Autenticación |
| Exposición de datos | AES-256 en BD | Datos |
| Pérdida de integridad | SHA-256 checksum | Datos |

---

## 5. INFRAESTRUCTURA Y DESPLIEGUE

### 5.1 Arquitectura de Despliegue

```mermaid
graph TB
    subgraph "Internet"
        USER[👤 Usuario]
    end
    
    subgraph "DMZ (Zona Desmilitarizada)"
        LB[⚖️ Load Balancer<br/>Nginx]
        SSL[🔒 SSL/TLS Termination]
    end
    
    subgraph "Application Zone"
        WEB1[🖥️ Web Server 1<br/>Nginx:80]
        WEB2[🖥️ Web Server 2<br/>Nginx:80]
        APP1[⚙️ App Server 1<br/>Flask:5000]
        APP2[⚙️ App Server 2<br/>Flask:5000]
    end
    
    subgraph "Data Zone (Private)"
        DB_MASTER[(💾 DB Master<br/>PostgreSQL)]
        DB_SLAVE[(💾 DB Replica<br/>Read-Only)]
        BACKUP[💿 Backups]
    end
    
    USER -->|HTTPS:443| SSL
    SSL --> LB
    LB --> WEB1
    LB --> WEB2
    WEB1 --> APP1
    WEB2 --> APP2
    APP1 --> DB_MASTER
    APP2 --> DB_MASTER
    APP1 -.->|Read| DB_SLAVE
    APP2 -.->|Read| DB_SLAVE
    DB_MASTER -.->|Replication| DB_SLAVE
    DB_MASTER -->|Daily Backup| BACKUP
    
    style SSL fill:#d4edda
    style LB fill:#cce5ff
    style DB_MASTER fill:#f8d7da
    style BACKUP fill:#fff3cd
```

### 5.2 Configuración de Servidor (Simplificada para el proyecto)

```mermaid
graph LR
    subgraph "Servidor Linux Ubuntu 20.04"
        NGINX[Nginx<br/>:443/:80]
        FLASK[Flask<br/>:5000]
        PG[(PostgreSQL<br/>:5432)]
        SSH[OpenSSH<br/>:22]
    end
    
    NGINX --> FLASK
    FLASK --> PG
    SSH -.->|Admin| FLASK
    SSH -.->|Admin| PG
    
    style NGINX fill:#d4edda
    style FLASK fill:#fff3cd
    style PG fill:#cce5ff
    style SSH fill:#f8d7da
```

---

## 6. ESCALABILIDAD Y EXTENSIBILIDAD

### 6.1 Puntos de Extensión

```mermaid
mindmap
  root((ESPE MedSafe))
    Nuevos Roles
      Enfermero
      Farmacéutico
      Laboratorista
    Nuevos Módulos
      Citas Médicas
      Recetas Electrónicas
      Resultados de Laboratorio
    Integraciones
      API Externa Laboratorios
      API Farmacias
      Sistema de Pagos
    Seguridad Avanzada
      2FA/MFA
      Biometría
      Blockchain para trazabilidad
```

### 6.2 Arquitectura Modular

El sistema está diseñado con módulos independientes que permiten:
- ✅ Agregar nuevos endpoints sin modificar existentes
- ✅ Cambiar implementaciones de cifrado sin cambiar la interfaz
- ✅ Escalar horizontalmente (más servidores)
- ✅ Migrar a microservicios en el futuro

---

## 7. TECNOLOGÍAS Y VERSIONES

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Backend Framework | Flask | 3.0.0 |
| ORM | SQLAlchemy | 2.0+ |
| Criptografía | cryptography | 41.0+ |
| Password Hash | bcrypt | 4.1+ |
| WSGI Server | Gunicorn | 21.2+ |
| Web Server | Nginx | 1.24+ |
| Base de Datos | PostgreSQL | 15+ |
| Python | CPython | 3.11+ |

---

## 8. VISUALIZACIÓN EN VS CODE

Para ver estos diagramas renderizados en VS Code:

1. Instala la extensión: **Markdown Preview Mermaid Support**
2. Abre este archivo
3. Presiona `Ctrl+Shift+V` (Vista previa de Markdown)
4. Los diagramas se renderizarán automáticamente

Para exportar a imagen:
- Usa la extensión **Mermaid Editor** 
- O copia el código Mermaid a https://mermaid.live/

---

**Fecha**: 8 de enero de 2026  
**Equipo**: ESPE MedSafe  
**Semana**: 2 - Diseño del Sistema
