# ESPE MedSafe - Semana 2: Diseño del Sistema
## Resumen Ejecutivo

---

## 📋 CONTENIDO DE LA CARPETA

Esta carpeta contiene todos los entregables de la **Semana 2: Diseño del Sistema** del proyecto ESPE MedSafe.

### Documentos Incluidos:

1. **01_Arquitectura_Sistema.md**
   - Diagramas Mermaid de arquitectura general
   - Arquitectura cliente-servidor
   - Capas de la aplicación (Presentación, Aplicación, Datos)
   - Flujos de datos con cifrado
   - Diagramas de seguridad
   - Infraestructura de despliegue

2. **02_Modelo_Base_Datos.md**
   - Diagrama Entidad-Relación (Mermaid)
   - Modelo lógico detallado de todas las tablas
   - Script SQL completo de creación (PostgreSQL)
   - Relaciones y cardinalidades
   - Consideraciones de seguridad en BD
   - Consultas SQL útiles

3. **03_Especificacion_API_REST.md**
   - Diagrama de endpoints
   - Especificación completa de todos los endpoints
   - Ejemplos de request/response
   - Autenticación JWT
   - Control de acceso por roles
   - Validaciones y rate limiting

4. **04_Bibliotecas_Criptograficas.md**
   - Selección justificada de bibliotecas
   - Ejemplos de código para cada biblioteca
   - Guía de instalación y configuración
   - Archivo requirements.txt completo
   - Mejores prácticas de seguridad

5. **README.md** (este archivo)
   - Guía de navegación de la documentación
   - Instrucciones para visualizar diagramas

---

## 🎯 ENTREGABLES DE LA SEMANA 2

### ✅ Completados:

1. **Diagrama de Arquitectura del Sistema** → [01_Arquitectura_Sistema.md](01_Arquitectura_Sistema.md)
2. **Modelo Entidad-Relación de Base de Datos** → [02_Modelo_Base_Datos.md](02_Modelo_Base_Datos.md)
3. **Especificación de API REST** → [03_Especificacion_API_REST.md](03_Especificacion_API_REST.md)
4. **Selección de Bibliotecas Criptográficas** → [04_Bibliotecas_Criptograficas.md](04_Bibliotecas_Criptograficas.md)

---

## 🖼️ VISUALIZACIÓN DE DIAGRAMAS

### Opción 1: VS Code (Recomendado)

1. **Instalar extensión**:
   - Abre VS Code
   - Ve a Extensions (Ctrl+Shift+X)
   - Busca: **"Markdown Preview Mermaid Support"**
   - Instala la extensión

2. **Ver diagramas**:
   - Abre cualquier archivo .md
   - Presiona `Ctrl+Shift+V` (Vista previa de Markdown)
   - Los diagramas Mermaid se renderizan automáticamente

### Opción 2: Online (Sin instalación)

1. Abre https://mermaid.live/
2. Copia el código Mermaid del documento
3. Pégalo en el editor online
4. Exporta como PNG/SVG/PDF

### Opción 3: GitHub/GitLab

- Los diagramas Mermaid se renderizan automáticamente al subir los archivos

---

## 📐 RESUMEN DE ARQUITECTURA

### Capas del Sistema:

```
┌─────────────────────────────────┐
│   CAPA DE PRESENTACIÓN         │
│   Frontend (HTML/CSS/JS)       │
└─────────────────────────────────┘
            ↕ HTTPS
┌─────────────────────────────────┐
│   CAPA DE APLICACIÓN           │
│   Backend (Flask/FastAPI)      │
│   - API REST                   │
│   - Autenticación (JWT)        │
│   - Módulo Criptográfico       │
│   - Auditoría                  │
└─────────────────────────────────┘
            ↕
┌─────────────────────────────────┐
│   CAPA DE DATOS                │
│   PostgreSQL / MySQL           │
│   - Datos cifrados (AES-256)   │
│   - Hash SHA-256 (integridad)  │
└─────────────────────────────────┘
```

---

## 🗄️ ESTRUCTURA DE BASE DE DATOS

### Tablas Principales:

| Tabla | Descripción | Campos Cifrados |
|-------|-------------|-----------------|
| **usuarios** | Credenciales y datos de usuarios | password_hash (bcrypt) |
| **pacientes** | Información de pacientes | alergias, antecedentes (AES-256) |
| **historias_clinicas** | Consultas médicas | sintomas, diagnostico, tratamiento (AES-256) |
| **recetas** | Medicamentos prescritos | - |
| **audit_logs** | Registro de auditoría | - |
| **claves_rsa** | Pares de claves RSA | private_key (AES-256) |

### Relaciones:

- `usuarios` (1) → (N) `pacientes` (Doctor gestiona múltiples pacientes)
- `pacientes` (1) → (N) `historias_clinicas` (Paciente tiene múltiples historias)
- `usuarios` (1) → (N) `historias_clinicas` (Doctor redacta múltiples historias)
- `historias_clinicas` (1) → (N) `recetas` (Historia contiene múltiples recetas)

---

## 🔌 API REST - ENDPOINTS PRINCIPALES

### Autenticación:
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/logout` - Cerrar sesión
- `GET /api/v1/auth/me` - Usuario actual

### Usuarios (Admin):
- `POST /api/v1/users` - Crear doctor
- `GET /api/v1/users` - Listar usuarios
- `PUT /api/v1/users/:id` - Actualizar usuario
- `DELETE /api/v1/users/:id` - Desactivar usuario

### Pacientes (Doctor):
- `POST /api/v1/patients` - Crear paciente
- `GET /api/v1/patients` - Listar pacientes
- `GET /api/v1/patients/:id` - Ver paciente
- `PUT /api/v1/patients/:id` - Actualizar paciente
- `DELETE /api/v1/patients/:id` - Eliminar paciente

### Historias Clínicas:
- `POST /api/v1/medical-records` - Crear historia
- `GET /api/v1/medical-records/patient/:id` - Historias de un paciente
- `GET /api/v1/medical-records/mine` - Mis historias (Paciente)
- `PUT /api/v1/medical-records/:id` - Actualizar historia

### Auditoría (Admin):
- `GET /api/v1/audit-logs` - Logs de auditoría
- `GET /api/v1/audit-logs/user/:id` - Logs de un usuario

---

## 📚 BIBLIOTECAS CRIPTOGRÁFICAS

### Principales:

1. **cryptography 41.0.5**
   - AES-256-CBC para cifrado simétrico
   - RSA-2048 para cifrado asimétrico y firma digital
   - Padding PKCS7 y OAEP

2. **bcrypt 4.1.2**
   - Hashing de contraseñas con salt automático
   - Factor de trabajo: 12 (4096 iteraciones)

3. **hashlib** (biblioteca estándar)
   - SHA-256 para verificación de integridad
   - Parte de Python, no requiere instalación

### Instalación:

```bash
# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🔐 TÉCNICAS CRIPTOGRÁFICAS IMPLEMENTADAS

| Técnica | Algoritmo | Uso en ESPE MedSafe |
|---------|-----------|---------------------|
| **Cifrado Simétrico** | AES-256-CBC | Historias clínicas, alergias, antecedentes |
| **Cifrado Asimétrico** | RSA-2048 | Firma digital de documentos (opcional) |
| **Hash de Contraseñas** | bcrypt (factor 12) | Autenticación de usuarios |
| **Verificación de Integridad** | SHA-256 | Detectar modificaciones no autorizadas |
| **Cifrados Clásicos** | César, Vigenère | Módulo educativo/demo |

---

## 📅 PRÓXIMOS PASOS (Semana 3)

1. **Desarrollo del backend**:
   - Implementar API REST con Flask
   - Crear módulo criptográfico funcional
   - Implementar autenticación JWT
   - Desarrollar CRUD de usuarios/pacientes/historias

2. **Pruebas**:
   - Probar cifrado/descifrado AES
   - Validar hashing bcrypt
   - Verificar integridad con SHA-256
   - Probar endpoints de API

**Entregable Semana 3**: Módulo criptográfico funcional

---

## 📖 CÓMO USAR ESTA DOCUMENTACIÓN

### Para Desarrolladores:

1. **Arquitectura** → Entender la estructura general del sistema
2. **Base de Datos** → Crear las tablas con el script SQL proporcionado
3. **API REST** → Implementar los endpoints siguiendo la especificación
4. **Bibliotecas** → Instalar dependencias y usar los ejemplos de código

### Para Presentación:

1. Exportar diagramas Mermaid a imágenes (PNG/SVG)
2. Usar los diagramas en la presentación PowerPoint
3. Incluir fragmentos de código relevantes

---

## 🎓 REFERENCIAS TÉCNICAS

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **cryptography**: https://cryptography.io/
- **bcrypt**: https://github.com/pyca/bcrypt/
- **Mermaid**: https://mermaid.js.org/

---

## 📞 INFORMACIÓN DEL PROYECTO

**Nombre**: ESPE MedSafe  
**Semana**: 2 - Diseño del Sistema  
**Estado**: ✅ COMPLETADA  
**Fecha**: 8 de enero de 2026  
**Equipo**: 3 estudiantes  
**Profesor**: Walter Fuertes, PhD.

---

## ✅ CHECKLIST DE ENTREGABLES

- [x] Diagrama de arquitectura del sistema
- [x] Modelo Entidad-Relación de BD
- [x] Script SQL de creación de tablas
- [x] Especificación completa de API REST
- [x] Selección y justificación de bibliotecas
- [x] Ejemplos de código criptográfico
- [x] Archivo requirements.txt
- [x] Documentación técnica detallada

---

**¡Listo para pasar a la Semana 3: Implementación del Backend! 🚀**
