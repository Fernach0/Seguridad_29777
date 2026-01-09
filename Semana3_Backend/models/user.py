"""
Modelo de Usuario
"""
from .base import db, TimestampMixin


class Usuario(db.Model, TimestampMixin):
    """Modelo de usuario del sistema"""
    
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(32), nullable=True)  # Nullable porque bcrypt incluye el salt en el hash
    rol = db.Column(db.String(20), nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False, index=True)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relaciones
    pacientes = db.relationship('Paciente', backref='doctor', lazy=True, 
                               foreign_keys='Paciente.doctor_id')
    historias_clinicas = db.relationship('HistoriaClinica', backref='doctor', 
                                        lazy=True, foreign_keys='HistoriaClinica.doctor_id')
    audit_logs = db.relationship('AuditLog', backref='usuario', lazy=True)
    clave_rsa = db.relationship('ClaveRSA', backref='usuario', uselist=False, 
                               cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Usuario {self.username} ({self.rol})>'
    
    def to_dict(self, include_sensitive=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'username': self.username,
            'rol': self.rol,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'cedula': self.cedula,
            'activo': self.activo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            data['salt'] = self.salt
        
        return data
    
    @property
    def nombre_completo(self):
        """Nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
