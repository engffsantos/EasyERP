# app/vendas/models/oportunidade.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from app.extensions import db
from app.vendas.models.cliente import Cliente  # necessário para back_populates
from app.core.models.user import Usuario


class Oportunidade(db.Model):
    __tablename__ = "oportunidades"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    valor_estimado = db.Column(NUMERIC(12, 2), nullable=False, default=0.00)
    status = db.Column(db.String(50), nullable=False, default='aberta')  # aberta, em negociação, ganha, perdida
    probabilidade = db.Column(db.Integer, nullable=False, default=0)  # 0 a 100 (%)

    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), nullable=False)
    usuario_responsavel = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos usando back_populates
    cliente = db.relationship("Cliente", back_populates="oportunidades", lazy=True)
    usuario = db.relationship("Usuario", backref="oportunidades", lazy=True)

    def __repr__(self):
        return f"<Oportunidade {self.titulo} - {self.status}>"
