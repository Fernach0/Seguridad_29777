# DEFINICIÓN DEL ALCANCE Y REQUISITOS
## ESPE MedSafe - Sistema de Gestión de Historias Clínicas Seguras

---

## 1. ALCANCE DEL PROYECTO

### 1.1 Descripción General
**ESPE MedSafe** es una plataforma web de gestión de historias clínicas médicas con enfoque en la seguridad y privacidad de datos sensibles de pacientes. El sistema implementa múltiples técnicas criptográficas para proteger la información médica, cumpliendo con estándares de seguridad en el sector salud.

### 1.2 Alcance Incluido (IN SCOPE)

#### Funcionalidades Principales:
1. **Sistema de Autenticación Multi-Rol**
   - Registro y login de usuarios (Administrador, Doctor, Paciente)
   - Autenticación segura con contraseñas hasheadas (bcrypt + salt)
   - Gestión de sesiones con tokens seguros

2. **Módulo de Administración**
   - Crear, editar y eliminar cuentas de doctores
   - Visualizar logs de auditoría del sistema
   - Gestionar permisos y roles

3. **Módulo de Gestión Médica (Doctores)**
   - CRUD completo de pacientes
   - Crear y editar historias clínicas
   - Redactar diagnósticos médicos
   - Recetar medicamentos
   - Visualizar historial completo de pacientes

4. **Módulo de Paciente (Lectura)**
   - Visualización de su propia historia clínica
   - Acceso a diagnósticos y recetas
   - Consulta de información personal médica

5. **Módulos de Seguridad Criptográfica**
   - Cifrado AES-256 de datos sensibles en base de datos
   - Cifrado RSA para comunicaciones críticas
   - Hashing SHA-256 para verificación de integridad
   - Implementación de bcrypt con salting para contraseñas
   - Módulo educativo de cifrados clásicos (César, Vigenère)

6. **Sistema de Auditoría**
   - Registro de accesos al sistema
   - Logs de modificaciones en historias clínicas
   - Trazabilidad de acciones por usuario

### 1.3 Alcance Excluido (OUT OF SCOPE)

- **NO** se implementará sistema de citas médicas
- **NO** se incluirá pasarela de pagos
- **NO** se desarrollará aplicación móvil nativa (solo web responsiva)
- **NO** se integrará con sistemas externos (laboratorios, farmacias)
- **NO** se implementará telemedicina o videollamadas
- **NO** se incluirá gestión de inventario de medicamentos
- **NO** se desarrollará sistema de imágenes médicas (DICOM)

---

## 2. REQUISITOS FUNCIONALES

### RF01: Gestión de Usuarios
- **RF01.1**: El sistema debe permitir el registro de nuevos usuarios con rol asignado
- **RF01.2**: El sistema debe validar credenciales de acceso (usuario y contraseña)
- **RF01.3**: El sistema debe cerrar sesiones automáticamente después de 30 minutos de inactividad
- **RF01.4**: El sistema debe mostrar diferentes interfaces según el rol del usuario

### RF02: Funcionalidades del Administrador
- **RF02.1**: El administrador puede crear cuentas de doctores con datos completos
- **RF02.2**: El administrador puede editar información de doctores existentes
- **RF02.3**: El administrador puede desactivar (no eliminar) cuentas de doctores
- **RF02.4**: El administrador puede consultar logs de auditoría con filtros por fecha, usuario y acción

### RF03: Funcionalidades del Doctor
- **RF03.1**: El doctor puede crear nuevos registros de pacientes
- **RF03.2**: El doctor puede editar información de pacientes existentes
- **RF03.3**: El doctor puede eliminar pacientes (con confirmación)
- **RF03.4**: El doctor puede crear nuevas historias clínicas con campos: síntomas, diagnóstico, tratamiento
- **RF03.5**: El doctor puede editar historias clínicas existentes (quedando registro del cambio)
- **RF03.6**: El doctor puede recetar medicamentos asociados a una consulta
- **RF03.7**: El doctor puede visualizar el historial completo de un paciente

### RF04: Funcionalidades del Paciente
- **RF04.1**: El paciente puede visualizar su información personal
- **RF04.2**: El paciente puede consultar su historial de consultas médicas
- **RF04.3**: El paciente puede ver diagnósticos y tratamientos prescritos
- **RF04.4**: El paciente NO puede editar ninguna información

### RF05: Cifrado y Seguridad
- **RF05.1**: El sistema debe cifrar los campos sensibles de historias clínicas con AES-256 antes de almacenar en BD
- **RF05.2**: El sistema debe usar RSA para intercambio de claves de sesión
- **RF05.3**: El sistema debe hashear todas las contraseñas con bcrypt (factor de trabajo: 12)
- **RF05.4**: El sistema debe generar un salt único por cada contraseña
- **RF05.5**: El sistema debe calcular hash SHA-256 de historias clínicas para detectar modificaciones
- **RF05.6**: El sistema debe incluir un módulo demostrativo de cifrados César y Vigenère

### RF06: Auditoría y Logs
- **RF06.1**: El sistema debe registrar cada inicio de sesión (usuario, fecha, hora, IP)
- **RF06.2**: El sistema debe registrar cada modificación en historias clínicas (quién, cuándo, qué cambió)
- **RF06.3**: El sistema debe mantener logs por al menos 90 días

---

## 3. REQUISITOS NO FUNCIONALES

### RNF01: Seguridad
- **RNF01.1**: El sistema debe usar HTTPS para todas las comunicaciones
- **RNF01.2**: Las contraseñas deben tener mínimo 8 caracteres, incluyendo mayúsculas, minúsculas, números y símbolos
- **RNF01.3**: El sistema debe proteger contra inyección SQL usando consultas parametrizadas
- **RNF01.4**: El sistema debe proteger contra XSS validando y escapando entradas
- **RNF01.5**: El sistema debe implementar protección CSRF en formularios
- **RNF01.6**: Las claves criptográficas deben almacenarse en variables de entorno, no en código

### RNF02: Rendimiento
- **RNF02.1**: El tiempo de respuesta para consultas simples debe ser menor a 2 segundos
- **RNF02.2**: El cifrado/descifrado de una historia clínica debe tomar menos de 500ms
- **RNF02.3**: El sistema debe soportar al menos 50 usuarios concurrentes

### RNF03: Usabilidad
- **RNF03.1**: La interfaz debe ser intuitiva y seguir principios de UX/UI
- **RNF03.2**: El sistema debe ser responsivo (adaptable a móviles y tablets)
- **RNF03.3**: Los mensajes de error deben ser claros y no revelar información sensible
- **RNF03.4**: El sistema debe usar el idioma español

### RNF04: Disponibilidad
- **RNF04.1**: El sistema debe estar disponible 99% del tiempo durante horario laboral (8am-6pm)
- **RNF04.2**: Debe existir un mecanismo de backup diario de la base de datos

### RNF05: Mantenibilidad
- **RNF05.1**: El código debe estar documentado con comentarios claros
- **RNF05.2**: El código debe seguir convenciones PEP 8 para Python
- **RNF05.3**: El sistema debe usar arquitectura modular para facilitar actualizaciones

### RNF06: Escalabilidad
- **RNF06.1**: La arquitectura debe permitir agregar nuevos roles en el futuro
- **RNF06.2**: El diseño de BD debe permitir agregar nuevos campos sin restructuración mayor

### RNF07: Compliance
- **RNF07.1**: El sistema debe ser auditable (logs completos)
- **RNF07.2**: Debe cumplir principios básicos de protección de datos personales sensibles

---

## 4. REQUISITOS TÉCNICOS

### 4.1 Backend
- **Lenguaje**: Python 3.9 o superior
- **Framework**: Flask o FastAPI
- **ORM**: SQLAlchemy
- **Bibliotecas criptográficas**:
  - `cryptography` (para AES, RSA)
  - `bcrypt` (para hashing de contraseñas)
  - `hashlib` (para SHA-256)

### 4.2 Frontend
- **Tecnología**: HTML5, CSS3, JavaScript
- **Framework opcional**: React, Vue.js o Bootstrap para diseño responsivo
- **Comunicación**: API REST (JSON)

### 4.3 Base de Datos
- **Motor**: PostgreSQL o MySQL
- **Características requeridas**:
  - Soporte para BLOB/TEXT (para datos cifrados)
  - Transacciones ACID
  - Índices para optimizar consultas

### 4.4 Infraestructura
- **Servidor web**: Nginx o Apache
- **Despliegue**: Linux (Ubuntu 20.04 o superior) con SELinux opcional
- **Acceso remoto**: OpenSSH configurado
- **Control de versiones**: Git + GitHub/GitLab

---

## 5. HISTORIAS DE USUARIO

### HU01: Inicio de Sesión Seguro
**Como** usuario del sistema  
**Quiero** iniciar sesión con mi usuario y contraseña  
**Para** acceder a las funcionalidades según mi rol  
**Criterios de aceptación**:
- La contraseña no se muestra mientras se escribe
- Si las credenciales son incorrectas, muestra mensaje genérico
- Si son correctas, redirige al dashboard correspondiente

### HU02: Creación de Paciente (Doctor)
**Como** doctor  
**Quiero** registrar un nuevo paciente en el sistema  
**Para** poder gestionar su historial médico  
**Criterios de aceptación**:
- Formulario con campos: nombre, apellido, cédula, fecha de nacimiento, contacto
- Validación de cédula única
- Confirmación visual de creación exitosa

### HU03: Consulta de Historia Clínica (Paciente)
**Como** paciente  
**Quiero** ver mi historial médico completo  
**Para** estar informado de mis diagnósticos y tratamientos  
**Criterios de aceptación**:
- Solo puedo ver MI propia información (no la de otros pacientes)
- Visualización clara de fecha, doctor, diagnóstico, tratamiento
- Descarga opcional en PDF

### HU04: Auditoría del Sistema (Administrador)
**Como** administrador  
**Quiero** ver todos los accesos al sistema  
**Para** detectar actividad sospechosa  
**Criterios de aceptación**:
- Tabla con: usuario, acción, fecha/hora, IP
- Filtros por fecha y usuario
- Exportación a CSV

### HU05: Cifrado Transparente (Sistema)
**Como** sistema  
**Quiero** cifrar automáticamente los diagnósticos antes de guardarlos  
**Para** proteger datos sensibles en la base de datos  
**Criterios de aceptación**:
- El usuario no nota el proceso de cifrado (transparente)
- Los datos en BD están cifrados (verificable)
- Al leer, se descifra automáticamente

---

## 6. PRIORIZACIÓN DE REQUISITOS (MoSCoW)

### Must Have (Debe tener - Prioridad Alta)
- Sistema de autenticación y roles
- CRUD de pacientes (doctor)
- Creación de historias clínicas
- Cifrado AES de datos sensibles
- Hashing bcrypt de contraseñas
- Base de datos funcional

### Should Have (Debería tener - Prioridad Media)
- Logs de auditoría
- Vista de lectura para pacientes
- SHA-256 para integridad
- RSA para autenticación
- Interfaz responsiva

### Could Have (Podría tener - Prioridad Baja)
- Módulo educativo de cifrados clásicos (César, Vigenère)
- Exportación de historias a PDF
- Configuración de SELinux
- Implementación de OpenSSH

### Won't Have (No tendrá - Fuera de alcance)
- Sistema de citas
- Integración con laboratorios
- Aplicación móvil nativa
- Telemedicina

---

## 7. RESTRICCIONES Y SUPUESTOS

### Restricciones
- **Tiempo**: 6 semanas de desarrollo
- **Equipo**: 3 desarrolladores
- **Presupuesto**: $0 (uso de software libre/open source)
- **Tecnología**: Debe usar Python como lenguaje principal

### Supuestos
- Los usuarios tienen conocimientos básicos de informática
- El servidor de despliegue será Linux
- Se cuenta con acceso a internet para bibliotecas y dependencias
- Los doctores tienen las credenciales creadas por el administrador

---

## 8. CRITERIOS DE ÉXITO

1. ✅ Sistema funcional con al menos 3 técnicas criptográficas implementadas
2. ✅ CRUD completo de pacientes e historias clínicas operativo
3. ✅ 3 roles diferenciados con permisos correctos
4. ✅ Datos sensibles cifrados en base de datos (verificable)
5. ✅ Contraseñas hasheadas con bcrypt (no legibles en BD)
6. ✅ Interfaz web funcional y accesible desde navegador
7. ✅ Logs de auditoría registrando acciones principales
8. ✅ Código documentado y en repositorio Git
9. ✅ Video demostrativo mostrando flujo completo
10. ✅ Artículo técnico en formato IEEE completado

---

## 9. RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Impacto | Estrategia de Mitigación |
|--------|--------------|---------|--------------------------|
| Problemas con bibliotecas criptográficas | Media | Alto | Investigar y probar bibliotecas en Semana 2 |
| Complejidad del cifrado asimétrico | Media | Medio | Dedicar tiempo extra en Semana 3 para RSA |
| Falta de experiencia en desarrollo web | Alta | Alto | Usar frameworks bien documentados (Flask) |
| Pérdida de datos durante desarrollo | Baja | Alto | Backups diarios del código y BD |
| Retraso en integración frontend-backend | Media | Medio | Definir API REST clara en Semana 2 |
| Problemas de compatibilidad en despliegue | Media | Medio | Usar Docker para entorno consistente |

---

**Fecha**: 8 de enero de 2026  
**Equipo**: ESPE MedSafe  
**Curso**: Ingeniería de Seguridad de Software  
**Profesor**: Walter Fuertes, PhD.
