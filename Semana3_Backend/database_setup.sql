-- ============================================
-- ESPE MedSafe - Script de Base de Datos
-- PostgreSQL 15+
-- ============================================

-- Crear base de datos (ejecutar primero como superusuario)
-- CREATE DATABASE espe_medsafe;
-- \c espe_medsafe;

-- ============================================
-- Tabla: usuarios
-- ============================================
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'doctor', 'paciente')),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para usuarios
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_cedula ON usuarios(cedula);
CREATE INDEX idx_usuarios_rol ON usuarios(rol);

-- ============================================
-- Tabla: pacientes
-- ============================================
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    grupo_sanguineo VARCHAR(5),
    alergias_encrypted BYTEA,
    alergias_iv BYTEA,
    antecedentes_encrypted BYTEA,
    antecedentes_iv BYTEA,
    doctor_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para pacientes
CREATE INDEX idx_pacientes_cedula ON pacientes(cedula);
CREATE INDEX idx_pacientes_doctor_id ON pacientes(doctor_id);
CREATE INDEX idx_pacientes_nombre ON pacientes(nombre);
CREATE INDEX idx_pacientes_apellido ON pacientes(apellido);

-- ============================================
-- Tabla: historias_clinicas
-- ============================================
CREATE TABLE IF NOT EXISTS historias_clinicas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT,
    fecha_consulta DATE NOT NULL,
    sintomas_encrypted BYTEA NOT NULL,
    diagnostico_encrypted BYTEA NOT NULL,
    tratamiento_encrypted BYTEA,
    notas_encrypted BYTEA,
    iv_aes BYTEA NOT NULL,
    hash_integridad VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para historias_clinicas
CREATE INDEX idx_historias_paciente_id ON historias_clinicas(paciente_id);
CREATE INDEX idx_historias_doctor_id ON historias_clinicas(doctor_id);
CREATE INDEX idx_historias_fecha_consulta ON historias_clinicas(fecha_consulta);

-- ============================================
-- Tabla: recetas
-- ============================================
CREATE TABLE IF NOT EXISTS recetas (
    id SERIAL PRIMARY KEY,
    historia_clinica_id INTEGER NOT NULL REFERENCES historias_clinicas(id) ON DELETE CASCADE,
    medicamento VARCHAR(200) NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    duracion_dias INTEGER NOT NULL,
    instrucciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para recetas
CREATE INDEX idx_recetas_historia_id ON recetas(historia_clinica_id);

-- ============================================
-- Tabla: audit_logs
-- ============================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    accion VARCHAR(50) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    ip_address VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para audit_logs
CREATE INDEX idx_audit_usuario_id ON audit_logs(usuario_id);
CREATE INDEX idx_audit_accion ON audit_logs(accion);
CREATE INDEX idx_audit_tabla ON audit_logs(tabla_afectada);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);

-- ============================================
-- Tabla: claves_rsa
-- ============================================
CREATE TABLE IF NOT EXISTS claves_rsa (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER UNIQUE NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    public_key TEXT NOT NULL,
    private_key_encrypted BYTEA NOT NULL,
    private_key_iv BYTEA NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para claves_rsa
CREATE INDEX idx_claves_usuario_id ON claves_rsa(usuario_id);

-- ============================================
-- Triggers para updated_at
-- ============================================

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para usuarios
CREATE TRIGGER update_usuarios_updated_at
    BEFORE UPDATE ON usuarios
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para pacientes
CREATE TRIGGER update_pacientes_updated_at
    BEFORE UPDATE ON pacientes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para historias_clinicas
CREATE TRIGGER update_historias_updated_at
    BEFORE UPDATE ON historias_clinicas
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Datos iniciales (opcional)
-- ============================================

-- Usuario administrador inicial
-- Contraseña: Admin123! (cambiar después del primer login)
-- El hash será generado por la aplicación

-- NOTA: Este INSERT se puede comentar si prefieres crear
-- el admin usando el script init_db.py de Python

/*
INSERT INTO usuarios (username, password_hash, salt, email, nombre, apellido, cedula, rol, activo)
VALUES (
    'admin',
    '$2b$12$ejemplo_hash_generado_por_aplicacion',
    '',
    'admin@espe.edu.ec',
    'Administrador',
    'Sistema',
    '0000000000',
    'admin',
    TRUE
);
*/

-- ============================================
-- Verificación
-- ============================================

-- Ver todas las tablas creadas
-- \dt

-- Ver estructura de una tabla específica
-- \d usuarios

-- Verificar datos
-- SELECT * FROM usuarios;

COMMIT;
