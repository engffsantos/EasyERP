import pytest
from unittest.mock import patch, MagicMock
import os
from werkzeug.datastructures import FileStorage
from app.shared.controllers.attachment_controller import AttachmentController
from app.shared.models.attachment import Attachment

def test_attachment_model():
    """Testa a criação de um modelo de anexo."""
    attachment = Attachment(
        filename="teste.pdf",
        filepath="/uploads/teste.pdf",
        filetype="application/pdf",
        filesize=1024,
        entity_type="ticket",
        entity_id=1,
        uploaded_by=1
    )
    
    assert attachment.filename == "teste.pdf"
    assert attachment.filepath == "/uploads/teste.pdf"
    assert attachment.filetype == "application/pdf"
    assert attachment.filesize == 1024
    assert attachment.entity_type == "ticket"
    assert attachment.entity_id == 1
    assert attachment.uploaded_by == 1

def test_save_attachment(app, db_session):
    """Testa o salvamento de um anexo no banco de dados."""
    with patch('app.shared.controllers.attachment_controller.secure_filename', return_value='teste_seguro.pdf'):
        with patch('app.shared.controllers.attachment_controller.os.path.join', return_value='/tmp/uploads/teste_seguro.pdf'):
            with patch('app.shared.controllers.attachment_controller.os.makedirs'):
                with patch('app.shared.controllers.attachment_controller.uuid.uuid4', return_value='unique-id'):
                    with patch('builtins.open', MagicMock()):
                        # Cria um arquivo de teste
                        test_file = FileStorage(
                            stream=open('/dev/null', 'rb'),
                            filename='teste.pdf',
                            content_type='application/pdf',
                        )
                        
                        # Chama o método para salvar o anexo
                        controller = AttachmentController()
                        result = controller.save_attachment(
                            file=test_file,
                            entity_type='ticket',
                            entity_id=1,
                            user_id=1
                        )
                        
                        # Verifica se o resultado é um dicionário com as informações do anexo
                        assert isinstance(result, dict)
                        assert result['filename'] == 'teste_seguro.pdf'
                        assert 'unique-id' in result['filepath']
                        assert result['filetype'] == 'application/pdf'
                        assert result['entity_type'] == 'ticket'
                        assert result['entity_id'] == 1

def test_get_attachments_for_entity():
    """Testa a obtenção de anexos para uma entidade específica."""
    with patch('app.shared.controllers.attachment_controller.Attachment.query') as mock_query:
        # Configura o mock para retornar uma lista de anexos
        mock_attachments = [
            MagicMock(id=1, filename='doc1.pdf', to_dict=lambda: {'id': 1, 'filename': 'doc1.pdf'}),
            MagicMock(id=2, filename='doc2.pdf', to_dict=lambda: {'id': 2, 'filename': 'doc2.pdf'})
        ]
        mock_query.filter_by.return_value.all.return_value = mock_attachments
        
        # Chama o método para obter os anexos
        controller = AttachmentController()
        result = controller.get_attachments_for_entity('ticket', 1)
        
        # Verifica se o resultado é uma lista com os anexos esperados
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['filename'] == 'doc1.pdf'
        assert result[1]['id'] == 2
        assert result[1]['filename'] == 'doc2.pdf'
        
        # Verifica se o método filter_by foi chamado com os parâmetros corretos
        mock_query.filter_by.assert_called_once_with(entity_type='ticket', entity_id=1)

def test_delete_attachment():
    """Testa a exclusão de um anexo."""
    with patch('app.shared.controllers.attachment_controller.Attachment.query') as mock_query:
        # Configura o mock para retornar um anexo
        mock_attachment = MagicMock(
            id=1, 
            filename='doc1.pdf',
            filepath='/uploads/doc1.pdf'
        )
        mock_query.get.return_value = mock_attachment
        
        # Mock para db.session
        mock_db = MagicMock()
        
        # Mock para os.remove
        with patch('app.shared.controllers.attachment_controller.os.remove') as mock_remove:
            # Chama o método para excluir o anexo
            controller = AttachmentController()
            controller.db = mock_db
            result = controller.delete_attachment(1)
            
            # Verifica se o anexo foi removido do banco de dados
            mock_db.delete.assert_called_once_with(mock_attachment)
            mock_db.commit.assert_called_once()
            
            # Verifica se o arquivo foi removido do sistema de arquivos
            mock_remove.assert_called_once_with('/uploads/doc1.pdf')
            
            # Verifica se o resultado é True
            assert result is True

def test_delete_attachment_not_found():
    """Testa a exclusão de um anexo que não existe."""
    with patch('app.shared.controllers.attachment_controller.Attachment.query') as mock_query:
        # Configura o mock para retornar None (anexo não encontrado)
        mock_query.get.return_value = None
        
        # Chama o método para excluir o anexo
        controller = AttachmentController()
        result = controller.delete_attachment(999)
        
        # Verifica se o resultado é False
        assert result is False
