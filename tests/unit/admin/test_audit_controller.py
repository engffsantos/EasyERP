import pytest
from unittest.mock import patch, MagicMock
from app.shared.models.audit_log import AuditLog
from app.shared.utils.audit_logger import log_audit, audit_log_decorator
from app.admin.controllers.audit_controller import AuditController

def test_audit_log_model():
    """Testa a criação de um modelo de log de auditoria."""
    audit_log = AuditLog(
        user_id=1,
        ip_address="192.168.1.1",
        action="create",
        entity_type="user",
        entity_id=2,
        details={"name": "Novo Usuário", "email": "teste@example.com"}
    )
    
    assert audit_log.user_id == 1
    assert audit_log.ip_address == "192.168.1.1"
    assert audit_log.action == "create"
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == 2
    assert audit_log.details == {"name": "Novo Usuário", "email": "teste@example.com"}

def test_log_audit_function(app, db_session):
    """Testa a função de registro de auditoria."""
    with patch('app.shared.utils.audit_logger.db.session') as mock_session:
        # Chama a função de registro de auditoria
        log_audit(
            user_id=1,
            ip_address="192.168.1.1",
            action="update",
            entity_type="ticket",
            entity_id=5,
            details={"status": "resolvido"}
        )
        
        # Verifica se a sessão do banco de dados foi usada corretamente
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        
        # Verifica se o objeto adicionado é um AuditLog com os valores corretos
        audit_log = mock_session.add.call_args[0][0]
        assert isinstance(audit_log, AuditLog)
        assert audit_log.user_id == 1
        assert audit_log.ip_address == "192.168.1.1"
        assert audit_log.action == "update"
        assert audit_log.entity_type == "ticket"
        assert audit_log.entity_id == 5
        assert audit_log.details == {"status": "resolvido"}

def test_audit_log_decorator():
    """Testa o decorator de registro de auditoria."""
    with patch('app.shared.utils.audit_logger.log_audit') as mock_log_audit:
        # Cria uma função de teste com o decorator
        @audit_log_decorator(entity_type="user", action="create")
        def test_function(user_id, name, email):
            return {"id": user_id, "name": name, "email": email}
        
        # Chama a função decorada
        result = test_function(user_id=3, name="Test User", email="test@example.com")
        
        # Verifica se a função original foi executada corretamente
        assert result == {"id": 3, "name": "Test User", "email": "test@example.com"}
        
        # Verifica se log_audit foi chamado com os parâmetros corretos
        mock_log_audit.assert_called_once()
        args, kwargs = mock_log_audit.call_args
        assert kwargs['user_id'] == 3
        assert kwargs['entity_type'] == "user"
        assert kwargs['action'] == "create"
        assert kwargs['details'] == {"name": "Test User", "email": "test@example.com"}

def test_get_audit_logs():
    """Testa a obtenção de logs de auditoria."""
    with patch('app.admin.controllers.audit_controller.AuditLog.query') as mock_query:
        # Configura o mock para retornar uma lista de logs
        mock_logs = [
            MagicMock(id=1, user_id=1, action="login", to_dict=lambda: {
                'id': 1, 'user_id': 1, 'action': 'login'
            }),
            MagicMock(id=2, user_id=2, action="update", to_dict=lambda: {
                'id': 2, 'user_id': 2, 'action': 'update'
            })
        ]
        mock_query.order_by.return_value.paginate.return_value = MagicMock(
            items=mock_logs,
            page=1,
            pages=1,
            total=2
        )
        
        # Chama o método para obter os logs
        controller = AuditController()
        result = controller.get_audit_logs(page=1, per_page=10)
        
        # Verifica se o resultado contém os logs esperados
        assert isinstance(result, dict)
        assert len(result['logs']) == 2
        assert result['logs'][0]['id'] == 1
        assert result['logs'][0]['user_id'] == 1
        assert result['logs'][0]['action'] == 'login'
        assert result['logs'][1]['id'] == 2
        assert result['logs'][1]['user_id'] == 2
        assert result['logs'][1]['action'] == 'update'
        assert result['page'] == 1
        assert result['total_pages'] == 1
        assert result['total_logs'] == 2

def test_filter_audit_logs():
    """Testa a filtragem de logs de auditoria."""
    with patch('app.admin.controllers.audit_controller.AuditLog.query') as mock_query:
        # Configura o mock para simular filtragem
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.filter.return_value = mock_filter
        mock_filter.order_by.return_value = mock_filter
        mock_filter.paginate.return_value = MagicMock(
            items=[],
            page=1,
            pages=0,
            total=0
        )
        
        # Chama o método para filtrar os logs
        controller = AuditController()
        controller.get_audit_logs(
            page=1,
            per_page=10,
            user_id=1,
            action="update",
            entity_type="ticket"
        )
        
        # Verifica se os filtros foram aplicados corretamente
        assert mock_query.filter.called
        assert mock_filter.filter.called
        assert mock_filter.order_by.called
        assert mock_filter.paginate.called
