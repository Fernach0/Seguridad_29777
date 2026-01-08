"""
Modelo de Historia Clínica y Receta
"""
from .base import db, TimestampMixin


class HistoriaClinica(db.Model, TimestampMixin):
    """Modelo de historia clínica"""
    
    __tablename__ = 'historias_clinicas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), 
                           nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='RESTRICT'), 
                         nullable=False, index=True)
    fecha_consulta = db.Column(db.Date, nullable=False, index=True)
    
    # Campos cifrados con AES-256
    sintomas_encrypted = db.Column(db.LargeBinary, nullable=False)
    diagnostico_encrypted = db.Column(db.LargeBinary, nullable=False)
    tratamiento_encrypted = db.Column(db.LargeBinary)
    notas_encrypted = db.Column(db.LargeBinary)
    
    # Vector de inicialización (IV) para AES
    iv_aes = db.Column(db.LargeBinary, nullable=False)
    
    # Hash de integridad SHA-256
    hash_integridad = db.Column(db.String(64), nullable=False)
    
    # Relaciones
    recetas = db.relationship('Receta', backref='historia_clinica', lazy=True,
                             cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<HistoriaClinica #{self.id} - Paciente {self.paciente_id}>'
    
    def to_dict(self, include_encrypted=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'doctor_id': self.doctor_id,
            'fecha_consulta': self.fecha_consulta.isoformat(),
            'hash_integridad': self.hash_integridad,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_encrypted:
            # Los datos cifrados se descifrarán en el controlador
            data['has_data'] = True
        
        return data


class Receta(db.Model):
    """Modelo de receta médica"""
    
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    historia_clinica_id = db.Column(db.Integer, 
                                   db.ForeignKey('historias_clinicas.id', ondelete='CASCADE'),
                                   nullable=False, index=True)
    medicamento = db.Column(db.String(200), nullable=False)
    dosis = db.Column(db.String(100), nullable=False)
    duracion_dias = db.Column(db.Integer, nullable=False)
    instrucciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Receta #{self.id} - {self.medicamento}>'
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'historia_clinica_id': self.historia_clinica_id,
            'medicamento': self.medicamento,
            'dosis': self.dosis,
            'duracion_dias': self.duracion_dias,
            'instrucciones': self.instrucciones,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
