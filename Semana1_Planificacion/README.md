# ESPE MedSafe - Resumen Ejecutivo
## Proyecto Final - Ingeniería de Seguridad de Software

---

## 📋 CONTENIDO DE LA CARPETA SEMANA 1

Esta carpeta contiene todos los entregables correspondientes a la **Semana 1: Planificación y Marco Teórico** del proyecto ESPE MedSafe.

### Documentos Incluidos:

1. **01_Revision_Conceptos_Criptograficos.md**
   - Explicación detallada de cifrado simétrico (AES, DES)
   - Cifrado asimétrico (RSA, ECC)
   - Funciones hash (SHA-256, bcrypt, salting)
   - Cifrados clásicos (César, Vigenère, XOR)
   - OpenSSH y SELinux
   - Referencias bibliográficas

2. **02_Alcance_y_Requisitos.md**
   - Alcance del proyecto (IN/OUT scope)
   - Requisitos funcionales detallados (RF01-RF06)
   - Requisitos no funcionales (seguridad, rendimiento, usabilidad)
   - Requisitos técnicos (stack tecnológico)
   - Historias de usuario
   - Priorización MoSCoW
   - Gestión de riesgos

3. **03_Propuesta_Proyecto_ESPE_MedSafe.md**
   - Propuesta formal de 1 página (según requisitos)
   - Descripción del proyecto
   - Objetivos generales y específicos
   - Arquitectura del sistema
   - Técnicas criptográficas seleccionadas
   - Roles y funcionalidades
   - Cronograma y entregables

4. **README.md** (este archivo)
   - Guía de navegación de la documentación

---

## 🎯 RESUMEN DEL PROYECTO

**Nombre**: ESPE MedSafe  
**Tipo**: Sistema Web de Gestión de Historias Clínicas Seguras  
**Duración**: 6 semanas  
**Equipo**: 3 estudiantes

### ¿Qué es ESPE MedSafe?

Es una plataforma web que permite gestionar historias clínicas médicas de forma segura, implementando múltiples técnicas criptográficas para proteger datos sensibles de pacientes.

### Roles del Sistema:

- **👨‍💼 Administrador**: Gestiona cuentas de doctores y audita el sistema
- **👨‍⚕️ Doctor**: CRUD completo de pacientes e historias clínicas
- **🧑‍🦱 Paciente**: Consulta su propia información médica (solo lectura)

### Técnicas Criptográficas Implementadas:

1. **AES-256** (Cifrado Simétrico) → Para cifrar diagnósticos y datos sensibles
2. **RSA-2048** (Cifrado Asimétrico) → Para autenticación y firma digital
3. **bcrypt + Salt** (Hash Seguro) → Para contraseñas
4. **SHA-256** → Verificación de integridad
5. **César/Vigenère** → Módulo educativo

---

## 🛠️ STACK TECNOLÓGICO

### Backend
- Python 3.9+
- Flask o FastAPI
- Bibliotecas: `cryptography`, `bcrypt`, `hashlib`

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap o React

### Base de Datos
- PostgreSQL o MySQL

### Infraestructura
- Linux Ubuntu 20.04+
- Nginx
- OpenSSH
- SELinux (opcional)

---

## 📅 CRONOGRAMA

| Semana | Actividad | Estado |
|--------|-----------|--------|
| 1 | Planificación y marco teórico | ✅ COMPLETADA |
| 2 | Diseño del sistema | ⏳ Próxima |
| 3 | Backend y algoritmos criptográficos | ⏳ Pendiente |
| 4 | Frontend e integración | ⏳ Pendiente |
| 5 | Integración completa y pruebas | ⏳ Pendiente |
| 6 | Artículo, video y presentación | ⏳ Pendiente |

---

## 📦 ENTREGABLES FINALES (Semana 6)

1. ✅ Código fuente completo (repositorio Git)
2. ✅ Base de datos funcional
3. ✅ Artículo técnico en formato IEEE
4. ✅ Video demostrativo (5 minutos)
5. ✅ Presentación PowerPoint
6. ✅ Documentación técnica

---

## 🔐 CARACTERÍSTICAS DE SEGURIDAD

- ✅ Cifrado de datos en reposo (AES-256)
- ✅ Cifrado de comunicaciones (HTTPS)
- ✅ Contraseñas hasheadas (bcrypt + salt único)
- ✅ Autenticación multi-rol (RBAC)
- ✅ Logs de auditoría completos
- ✅ Protección contra SQL Injection, XSS, CSRF
- ✅ Verificación de integridad (SHA-256)

---

## 📚 PRÓXIMOS PASOS (Semana 2)

1. Diseñar la arquitectura detallada del sistema
2. Crear el modelo de base de datos (diagrama ER)
3. Definir la API REST (endpoints y métodos)
4. Seleccionar versiones específicas de bibliotecas
5. Configurar el entorno de desarrollo

**Entregables Semana 2**:
- Diagrama de arquitectura del sistema
- Modelo Entidad-Relación de la base de datos
- Especificación de API REST

---

## 👥 EQUIPO DE DESARROLLO

- Estudiante 1: [Luis Cueva]
- Estudiante 2: [Mateo Condor]
- Estudiante 3: [Gabriel Reinoso]

**Profesor**: Walter Fuertes, PhD.  
**Curso**: Ingeniería de Seguridad de Software  
**Universidad**: ESPE - Universidad de las Fuerzas Armadas

---

## 📖 CÓMO USAR ESTA DOCUMENTACIÓN

1. **Empieza por**: `03_Propuesta_Proyecto_ESPE_MedSafe.md` para tener una visión general
2. **Profundiza en**: `01_Revision_Conceptos_Criptograficos.md` para entender la teoría
3. **Planifica con**: `02_Alcance_y_Requisitos.md` para guiar el desarrollo

---

## 📞 CONTACTO

Para consultas sobre el proyecto, contactar a través de la plataforma del curso o correo institucional.

---

**Fecha de Creación**: 8 de enero de 2026  
**Última Actualización**: 8 de enero de 2026  
**Versión**: 1.0

---

## 🎓 REFERENCIAS PRINCIPALES

1. NIST. (2001). *Advanced Encryption Standard (AES)*. FIPS PUB 197.
2. Rivest, R., Shamir, A., & Adleman, L. (1978). *A method for obtaining digital signatures and public-key cryptosystems*.
3. NIST. (2015). *SHA-3 Standard*. FIPS PUB 202.
4. Provos, N., & Mazières, D. (1999). *A Future-Adaptable Password Scheme*.
5. Katz, J., & Lindell, Y. (2020). *Introduction to Modern Cryptography* (3rd ed.).

---

**¡Éxito en el desarrollo de ESPE MedSafe! 🚀**
