"""
Modelo de Paciente
"""
from .base import db, TimestampMixin


class Paciente(db.Model, TimestampMixin):
    """Modelo de paciente"""
    
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(10))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    grupo_sanguineo = db.Column(db.String(5))
    
    # Campos cifrados
    alergias_encrypted = db.Column(db.LargeBinary)  # Cifrado con AES
    alergias_iv = db.Column(db.LargeBinary)  # IV para AES
    antecedentes_encrypted = db.Column(db.LargeBinary)  # Cifrado con AES
    antecedentes_iv = db.Column(db.LargeBinary)  # IV para AES
    
    # Relación con doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    
    # Relaciones
    historias_clinicas = db.relationship('HistoriaClinica', backref='paciente', 
                                        lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Paciente {self.nombre} {self.apellido} - {self.cedula}>'
    
    def to_dict(self, include_encrypted=False):
        """Convertir a diccionario"""
        from datetime import date
        
        # Calcular edad
        today = date.today()
        edad = today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
        
        data = {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat(),
            'edad': edad,
            'genero': self.genero,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'grupo_sanguineo': self.grupo_sanguineo,
            'doctor_id': self.doctor_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_encrypted:
            # Los datos cifrados se descifrarán en el controlador
            data['has_alergias'] = bool(self.alergias_encrypted)
            data['has_antecedentes'] = bool(self.antecedentes_encrypted)
        
        return data
    
    @property
    def nombre_completo(self):
        """Nombre completo del paciente"""
        return f"{self.nombre} {self.apellido}"
