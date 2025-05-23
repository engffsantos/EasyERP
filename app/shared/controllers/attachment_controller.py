# app/shared/controllers/attachment_controller.py
import os
from flask import request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app.extensions import db
from app.shared.models.attachment import Attachment
from app.service_desk.models.ticket import Ticket
from app.vendas.models.cliente import Cliente
from datetime import datetime
import uuid

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "doc", "docx", "xls", "xlsx", "ppt", "pptx"}

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

class AttachmentController:
    
    @staticmethod
    def upload_attachment(parent_type, parent_id):
        """Realiza o upload de um anexo para um Ticket ou Cliente"""
        if parent_type not in ["ticket", "cliente"]:
            return jsonify({"error": "Tipo de entidade pai inválido"}), 400
        
        if "file" not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        file = request.files["file"]
        
        if file.filename == "":
            return jsonify({"error": "Nome de arquivo vazio"}), 400
        
        if file and allowed_file(file.filename):
            # Gerar nome de arquivo seguro e único
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4()}.{extension}"
            
            # Determinar o caminho de armazenamento
            upload_folder = current_app.config.get("UPLOAD_FOLDER", "/home/ubuntu/easyerp/uploads")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            filepath = os.path.join(upload_folder, unique_filename)
            
            try:
                file.save(filepath)
                filesize = os.path.getsize(filepath)
                mimetype = file.mimetype
                
                # Criar registro no banco de dados
                new_attachment = Attachment(
                    filename=original_filename,
                    filepath=filepath,
                    mimetype=mimetype,
                    filesize=filesize
                    # uploaded_by_id=current_user.id # Adicionar se houver autenticação
                )
                
                # Associar ao pai (Ticket ou Cliente)
                if parent_type == "ticket":
                    ticket = Ticket.query.get_or_404(parent_id)
                    new_attachment.ticket_id = ticket.id
                elif parent_type == "cliente":
                    cliente = Cliente.query.get_or_404(parent_id)
                    new_attachment.cliente_id = cliente.id
                
                db.session.add(new_attachment)
                db.session.commit()
                
                return jsonify({
                    "message": "Arquivo enviado com sucesso",
                    "attachment_id": new_attachment.id,
                    "filename": new_attachment.filename
                }), 201
                
            except Exception as e:
                db.session.rollback()
                # Remover arquivo se o commit falhar
                if os.path.exists(filepath):
                    os.remove(filepath)
                current_app.logger.error(f"Erro ao salvar anexo: {e}")
                return jsonify({"error": "Erro interno ao salvar o arquivo"}), 500
        else:
            return jsonify({"error": "Tipo de arquivo não permitido"}), 400

    @staticmethod
    def download_attachment(attachment_id):
        """Permite o download de um anexo pelo ID"""
        attachment = Attachment.query.get_or_404(attachment_id)
        upload_folder = os.path.dirname(attachment.filepath)
        filename = os.path.basename(attachment.filepath)
        
        try:
            return send_from_directory(
                upload_folder,
                filename,
                as_attachment=True,
                download_name=attachment.filename # Usa o nome original para download
            )
        except FileNotFoundError:
            return jsonify({"error": "Arquivo não encontrado no servidor"}), 404
        except Exception as e:
            current_app.logger.error(f"Erro ao baixar anexo {attachment_id}: {e}")
            return jsonify({"error": "Erro interno ao baixar o arquivo"}), 500

    @staticmethod
    def delete_attachment(attachment_id):
        """Exclui um anexo pelo ID"""
        attachment = Attachment.query.get_or_404(attachment_id)
        filepath = attachment.filepath
        
        try:
            db.session.delete(attachment)
            db.session.commit()
            
            # Remover o arquivo físico
            if os.path.exists(filepath):
                os.remove(filepath)
                
            return jsonify({"message": "Anexo excluído com sucesso"}), 200
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Erro ao excluir anexo {attachment_id}: {e}")
            return jsonify({"error": "Erro interno ao excluir o anexo"}), 500
