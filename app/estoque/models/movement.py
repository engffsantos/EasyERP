# app/estoque/models/movement.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from app.extensions import db


class MovimentacaoEstoque(db.Model):
    __tablename__ = "movimentacoes_estoque"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tipo = db.Column(db.String(20), nullable=False)  # entrada, saida, ajuste, transferencia
    motivo = db.Column(db.String(255), nullable=True)

    produto_id = db.Column(UUID(as_uuid=True), db.ForeignKey("produtos.id"), nullable=False)

    armazem_origem_id = db.Column(UUID(as_uuid=True), db.ForeignKey("armazens.id"), nullable=True)
    armazem_destino_id = db.Column(UUID(as_uuid=True), db.ForeignKey("armazens.id"), nullable=True)

    quantidade = db.Column(NUMERIC(12, 2), nullable=False)

    data_movimentacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    produto = db.relationship("Produto", backref="movimentacoes", lazy=True)
    usuario = db.relationship("Usuario", backref="movimentacoes_estoque", lazy=True)
    armazem_origem = db.relationship("Armazem", foreign_keys=[armazem_origem_id], lazy=True)
    armazem_destino = db.relationship("Armazem", foreign_keys=[armazem_destino_id], lazy=True)

    def __repr__(self):
        return f"<MovimentacaoEstoque {self.tipo} - {self.quantidade} de {self.produto.nome}>"
