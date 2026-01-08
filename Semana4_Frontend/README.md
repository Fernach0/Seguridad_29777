# ESPE MedSafe - Frontend React

Frontend desarrollado con React + Vite para el sistema ESPE MedSafe.

## 🚀 Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

## 📝 Configuración

El frontend se conecta al backend en `http://localhost:5000/api/v1`

Credenciales por defecto:
- Username: `admin`
- Password: `Admin123!`

## 🎯 Características

- ✅ Autenticación con JWT
- ✅ Control de acceso por roles
- ✅ Dashboard interactivo
- ✅ Gestión de usuarios (Admin)
- ✅ Gestión de pacientes (Doctor)
- ✅ Historias clínicas con cifrado
- ✅ Demos educativas de criptografía
- ✅ Auditoría del sistema

## 🛠️ Tecnologías

- React 18.2
- React Router 6.20
- Bootstrap 5.3
- Axios 1.6
- Vite 5.0

## 📦 Estructura

```
src/
├── components/       # Componentes reutilizables
├── contexts/        # Context API (Auth)
├── pages/           # Páginas principales
├── services/        # Servicios API
├── App.jsx          # Componente principal
└── main.jsx         # Punto de entrada
```

## 🔗 Endpoints del Backend

- POST `/auth/login` - Iniciar sesión
- GET `/auth/me` - Usuario actual
- GET `/users` - Listar usuarios
- GET `/patients` - Listar pacientes
- GET `/medical-records` - Historias clínicas
- POST `/crypto/*` - Demos criptográficas
- GET `/audit` - Logs de auditoría

## 📚 Próximos Pasos

Completar la implementación de las páginas pendientes con formularios y tablas interactivas.
