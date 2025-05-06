# app/service_desk/models/asset.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Ativo(db.Model):
    __tablename__ = "ativos"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)  # exemplo: notebook, impressora, servidor
    numero_serie = db.Column(db.String(100), nullable=True, unique=True)
    localizacao = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="ativo")  # ativo, em manutenção, desativado

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Ativo {self.nome} ({self.tipo}) - {self.status}>"
