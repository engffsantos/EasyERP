# app/service_desk/models/ticket.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="aberto")  # aberto, em atendimento, resolvido, fechado
    prioridade = db.Column(db.String(20), nullable=False, default="normal")  # baixa, normal, alta, crítica

    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)
    ativo_id = db.Column(UUID(as_uuid=True), db.ForeignKey("ativos.id"), nullable=True)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    usuario = db.relationship("Usuario", backref="tickets", lazy=True)
    ativo = db.relationship("Ativo", backref="tickets", lazy=True)

    def __repr__(self):
        return f"<Ticket {self.titulo} - {self.status}>"
