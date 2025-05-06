# app/vendas/models/interacao.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db

class Interacao(db.Model):
    __tablename__ = "interacoes"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo = db.Column(db.String(20), nullable=False)  # 'email', 'ligacao', 'reuniao'
    descricao = db.Column(db.Text, nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    cliente_id = db.Column(UUID(as_uuid=True), db.ForeignKey("clientes.id"), nullable=False)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Interacao {self.tipo} com cliente {self.cliente_id} em {self.data}>"
