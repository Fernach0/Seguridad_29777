# PROPUESTA DE PROYECTO - SEMANA 1
## ESPE MedSafe: Sistema de Gestión de Historias Clínicas con Seguridad Criptográfica

**Universidad de las Fuerzas Armadas - ESPE**  
**Curso**: Ingeniería de Seguridad de Software  
**Profesor**: Walter Fuertes, PhD.  
**Fecha**: 8 de enero de 2026

---

## 1. INFORMACIÓN DEL PROYECTO

**Nombre del Proyecto**: ESPE MedSafe  
**Tipo de Aplicación**: Plataforma Web  
**Duración**: 6 semanas  
**Equipo**: 3 estudiantes

---

## 2. DESCRIPCIÓN DEL PROYECTO

**ESPE MedSafe** es un sistema web de gestión de historias clínicas médicas que implementa múltiples técnicas criptográficas para garantizar la confidencialidad, integridad y disponibilidad de información sensible de pacientes. El sistema permite a administradores, doctores y pacientes interactuar con datos médicos de forma segura, cumpliendo con principios de protección de datos en el sector salud.

### Problema a Resolver
Los sistemas de salud manejan información altamente sensible que requiere protección robusta. Muchos sistemas no implementan cifrado adecuado, dejando expuestos diagnósticos, tratamientos y datos personales. ESPE MedSafe aborda esta problemática mediante la implementación de criptografía moderna integrada en cada capa del sistema.

---

## 3. OBJETIVOS

### Objetivo General
Desarrollar una plataforma web funcional que gestione historias clínicas médicas implementando al menos tres técnicas criptográficas diferentes, con arquitectura cliente-servidor, base de datos segura y roles de usuario diferenciados.

### Objetivos Específicos
1. Implementar cifrado simétrico AES-256 para proteger datos sensibles en la base de datos.
2. Integrar cifrado asimétrico RSA-2048 para autenticación y firma digital de documentos médicos.
3. Utilizar hashing bcrypt con salting para el almacenamiento seguro de contraseñas.
4. Desarrollar un sistema CRUD completo para la gestión de pacientes e historias clínicas.
5. Crear una interfaz web intuitiva siguiendo principios de UX/UI y diseño centrado en el usuario.
6. Implementar un sistema de auditoría con logs de acceso y modificaciones.
7. Demostrar el funcionamiento de cifrados clásicos (César, Vigenère) con fines educativos.

---

## 4. ARQUITECTURA DEL SISTEMA

### 4.1 Componentes Principales

**Frontend (Cliente Web)**
- HTML5, CSS3, JavaScript
- Framework: Bootstrap o React para diseño responsivo
- Comunicación: Peticiones HTTP/HTTPS a API REST

**Backend (Servidor de Aplicación)**
- Lenguaje: Python 3.9+
- Framework: Flask o FastAPI
- Módulos criptográficos: `cryptography`, `bcrypt`, `hashlib`
- Gestión de sesiones: Flask-Session o JWT

**Base de Datos**
- Motor: PostgreSQL o MySQL
- Almacenamiento: Datos cifrados en campos BLOB/TEXT
- Esquema: Usuarios, Pacientes, HistoriasClinicas, Logs

**Seguridad Adicional**
- OpenSSH para acceso remoto seguro al servidor
- SELinux (opcional) para hardening del sistema operativo

### 4.2 Flujo de Datos
1. Usuario ingresa datos en el frontend
2. Frontend envía solicitud HTTPS al backend
3. Backend valida y aplica cifrado según sea necesario
4. Datos cifrados se almacenan en la base de datos
5. Al recuperar datos, el backend descifra antes de enviar al frontend
6. Cada acción se registra en logs de auditoría

---

## 5. TÉCNICAS CRIPTOGRÁFICAS SELECCIONADAS

### Técnica 1: Cifrado Simétrico - AES-256
- **Aplicación**: Cifrado de diagnósticos, tratamientos y notas médicas en la base de datos.
- **Justificación**: Rápido, eficiente y altamente seguro para datos en reposo.

### Técnica 2: Cifrado Asimétrico - RSA-2048
- **Aplicación**: Autenticación de usuarios y firma digital de historias clínicas.
- **Justificación**: Permite verificar la integridad y autenticidad de documentos médicos.

### Técnica 3: Hash Seguro - bcrypt con Salting
- **Aplicación**: Almacenamiento de contraseñas de todos los usuarios del sistema.
- **Justificación**: Resistente a ataques de fuerza bruta y rainbow tables.

### Técnicas Adicionales (Demostración)
- **SHA-256**: Verificación de integridad de historias clínicas.
- **Cifrados Clásicos (César, Vigenère)**: Módulo educativo para mostrar evolución histórica de la criptografía.

---

## 6. ROLES Y FUNCIONALIDADES

### Rol 1: Administrador
- Crear cuentas de doctores
- Editar y desactivar usuarios
- Visualizar logs de auditoría completos
- Gestionar permisos del sistema

### Rol 2: Doctor
- CRUD completo de pacientes
- Crear y editar historias clínicas
- Redactar diagnósticos y prescribir tratamientos
- Consultar historial completo de pacientes

### Rol 3: Paciente (Lectura)
- Visualizar su propia información médica
- Consultar diagnósticos y tratamientos recibidos
- Sin permisos de edición

---

## 7. TECNOLOGÍAS Y HERRAMIENTAS

| Categoría | Tecnología/Herramienta |
|-----------|------------------------|
| Backend | Python 3.9+, Flask/FastAPI |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap/React |
| Base de Datos | PostgreSQL o MySQL |
| Criptografía | cryptography, bcrypt, hashlib |
| Control de Versiones | Git + GitHub/GitLab |
| Servidor Web | Nginx |
| Sistema Operativo | Linux Ubuntu 20.04+ |
| Contenedores (opcional) | Docker |

---

## 8. ENTREGABLES

1. **Código fuente completo** (repositorio Git organizado)
2. **Base de datos funcional** con datos de prueba
3. **Artículo técnico** en formato IEEE (Introducción, Metodología, Resultados, Discusión, Conclusiones)
4. **Video demostrativo** (5 minutos) mostrando flujo completo del sistema
5. **Presentación PowerPoint** (10 minutos) con explicación técnica
6. **Documentación técnica** (manual de instalación, arquitectura, API)

---

## 9. CRONOGRAMA RESUMIDO

- **Semana 1**: Planificación, revisión de conceptos criptográficos, definición de requisitos ✅
- **Semana 2**: Diseño de arquitectura, modelo de base de datos, selección de bibliotecas
- **Semana 3**: Desarrollo del backend y módulos criptográficos
- **Semana 4**: Desarrollo del frontend e integración con API
- **Semana 5**: Integración completa, pruebas de seguridad, refinamiento
- **Semana 6**: Documentación, artículo, video y preparación de presentación

---

## 10. VALOR Y APORTE

### Valor Académico
- Aplicación práctica de conceptos de criptografía y seguridad de software
- Experiencia en desarrollo full-stack con enfoque en seguridad
- Cumplimiento de estándares de protección de datos sensibles

### Valor Técnico
- Sistema funcional que puede servir como base para proyectos reales en el sector salud
- Implementación correcta de múltiples algoritmos criptográficos
- Arquitectura modular y escalable

### Innovación
- Integración de cifrado clásico y moderno en un mismo sistema
- Módulo educativo interactivo sobre criptografía
- Logs de auditoría para compliance y trazabilidad

---

## 11. CONCLUSIONES PRELIMINARES

ESPE MedSafe representa una propuesta viable y ambiciosa que cumple con todos los requisitos del proyecto final. La combinación de gestión de historias clínicas con seguridad criptográfica robusta lo convierte en un caso de estudio relevante para la ingeniería de software seguro. El equipo cuenta con 6 semanas para implementar un prototipo funcional que demuestre la aplicación práctica de los conceptos aprendidos en el curso.

La jerarquía de roles (Administrador, Doctor, Paciente) está claramente definida y permite demostrar control de acceso basado en roles (RBAC). Las tres técnicas criptográficas obligatorias (AES, RSA, bcrypt) están justificadas técnicamente y cubren diferentes necesidades: confidencialidad, autenticación e integridad.

---

**Firmas del Equipo**:

_______________________  
Luis Cueva

_______________________  
Mateo Condor

_______________________  
Gabriel Reinoso

---

**Fecha de Entrega**: 8 de enero de 2026  
**Próxima Entrega (Semana 2)**: Diagrama de arquitectura + modelo de BD
