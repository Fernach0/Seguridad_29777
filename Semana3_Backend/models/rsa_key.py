"""
Modelo de Claves RSA
"""
from .base import db


class ClaveRSA(db.Model):
    """Modelo de par de claves RSA por usuario"""
    
    __tablename__ = 'claves_rsa'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'),
                          unique=True, nullable=False, index=True)
    public_key = db.Column(db.Text, nullable=False)  # PEM format
    private_key_encrypted = db.Column(db.Text, nullable=False)  # Cifrada con AES
    private_key_iv = db.Column(db.LargeBinary)  # IV para AES
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime)  # Opcional: rotación de claves
    
    def __repr__(self):
        return f'<ClaveRSA User {self.usuario_id}>'
    
    def to_dict(self, include_private=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'public_key': self.public_key,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
        
        if include_private:
            # Solo incluir clave privada si es absolutamente necesario
            data['has_private_key'] = bool(self.private_key_encrypted)
        
        return data
