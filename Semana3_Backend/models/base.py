"""
Base de datos y configuración de SQLAlchemy
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instancia de SQLAlchemy
db = SQLAlchemy()


class TimestampMixin:
    """Mixin para agregar timestamps a los modelos"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )
