# app/shared/models/attachment.py
from app.extensions import db
from datetime import datetime

class Attachment(db.Model):
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False, unique=True)
    mimetype = db.Column(db.String(100), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relacionamentos polimórficos (para associar a Tickets ou Clientes)
    # Usaremos uma abordagem simples com colunas separadas por enquanto
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    
    # Relacionamento com usuário (opcional, se quisermos saber quem fez upload)
    uploaded_by = db.relationship('User', backref='uploaded_attachments')
    
    def __repr__(self):
        return f'<Attachment {self.filename}>'
