"""
Modelo de Log de Auditoría
"""
from .base import db


class AuditLog(db.Model):
    """Modelo de log de auditoría"""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'), 
                          index=True)
    accion = db.Column(db.String(50), nullable=False, index=True)
    tabla_afectada = db.Column(db.String(50), index=True)
    registro_id = db.Column(db.Integer)
    datos_anteriores = db.Column(db.Text)  # JSON
    datos_nuevos = db.Column(db.Text)  # JSON
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                         nullable=False, index=True)
    
    def __repr__(self):
        return f'<AuditLog #{self.id} - {self.accion} by User {self.usuario_id}>'
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'accion': self.accion,
            'tabla_afectada': self.tabla_afectada,
            'registro_id': self.registro_id,
            'datos_anteriores': self.datos_anteriores,
            'datos_nuevos': self.datos_nuevos,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
