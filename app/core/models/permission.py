# app/core/models/permission.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

# Tabela associativa entre perfis e permissões
class PerfilPermissao(db.Model):
    __tablename__ = "perfil_permissao"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    perfil_id = db.Column(UUID(as_uuid=True), db.ForeignKey("perfis.id"), nullable=False)
    permissao_id = db.Column(UUID(as_uuid=True), db.ForeignKey("permissoes.id"), nullable=False)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Permissao(db.Model):
    __tablename__ = "permissoes"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relacionamento inverso com perfis via tabela associativa
    perfis = db.relationship(
        "Perfil",
        secondary="perfil_permissao",
        backref=db.backref("permissoes", lazy="dynamic"),
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Permissao {self.nome}>"
