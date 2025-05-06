# app/core/models/user.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref

from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    perfil_id = db.Column(UUID(as_uuid=True), db.ForeignKey("perfis.id"), nullable=False)
    perfil = db.relationship("Perfil", backref=backref("usuarios", lazy=True))

    supervisor_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=True)
    supervisor = db.relationship("Usuario", remote_side=[id], backref="subordinados", lazy=True)

    ativo = db.Column(db.Boolean, default=True, nullable=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Usuario {self.nome} - {self.email}>"
