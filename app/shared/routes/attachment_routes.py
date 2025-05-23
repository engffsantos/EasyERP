# app/shared/routes/attachment_routes.py
from flask import Blueprint
from app.shared.controllers.attachment_controller import AttachmentController

# Criação do blueprint para anexos
attachment_bp = Blueprint("attachments", __name__, url_prefix="/attachments")

# Rota para upload de anexo para um Ticket
attachment_bp.route("/upload/ticket/<int:parent_id>", methods=["POST"])(AttachmentController.upload_attachment)

# Rota para upload de anexo para um Cliente
attachment_bp.route("/upload/cliente/<int:parent_id>", methods=["POST"])(AttachmentController.upload_attachment)

# Rota para download de anexo
attachment_bp.route("/download/<int:attachment_id>", methods=["GET"])(AttachmentController.download_attachment)

# Rota para excluir anexo
attachment_bp.route("/delete/<int:attachment_id>", methods=["DELETE"])(AttachmentController.delete_attachment)

def init_app(app):
    """Inicializa o módulo de anexos na aplicação Flask"""
    app.register_blueprint(attachment_bp)
