import pytest
from unittest.mock import patch
from app.dashboard.controllers.dashboard_controller import DashboardController

def test_get_financial_data():
    """Testa se os dados financeiros são retornados corretamente."""
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_financial_data_from_db') as mock_db:
        # Configura o mock para retornar dados de teste
        mock_db.return_value = {
            'labels': ['Jan', 'Fev', 'Mar'],
            'receitas': [1000, 1200, 1500],
            'despesas': [800, 900, 1100]
        }
        
        # Chama o método real que usa o mock internamente
        controller = DashboardController()
        result = controller.get_financial_data()
        
        # Verifica se o resultado contém os dados esperados
        assert 'labels' in result
        assert 'datasets' in result
        assert len(result['datasets']) == 2
        assert result['datasets'][0]['label'] == 'Receitas'
        assert result['datasets'][1]['label'] == 'Despesas'
        assert result['datasets'][0]['data'] == [1000, 1200, 1500]
        assert result['datasets'][1]['data'] == [800, 900, 1100]
        
        # Verifica se o método de banco de dados foi chamado
        mock_db.assert_called_once()

def test_get_sales_data():
    """Testa se os dados de vendas são retornados corretamente."""
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_sales_data_from_db') as mock_db:
        # Configura o mock para retornar dados de teste
        mock_db.return_value = {
            'labels': ['Em Andamento', 'Ganhas', 'Perdidas', 'Novas'],
            'data': [5, 10, 3, 7]
        }
        
        # Chama o método real que usa o mock internamente
        controller = DashboardController()
        result = controller.get_sales_data()
        
        # Verifica se o resultado contém os dados esperados
        assert 'labels' in result
        assert 'datasets' in result
        assert len(result['datasets']) == 1
        assert result['datasets'][0]['data'] == [5, 10, 3, 7]
        
        # Verifica se o método de banco de dados foi chamado
        mock_db.assert_called_once()

def test_get_inventory_data():
    """Testa se os dados de estoque são retornados corretamente."""
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_inventory_data_from_db') as mock_db:
        # Configura o mock para retornar dados de teste
        mock_db.return_value = {
            'labels': ['Produto A', 'Produto B', 'Produto C'],
            'data': [150, 75, 25]
        }
        
        # Chama o método real que usa o mock internamente
        controller = DashboardController()
        result = controller.get_inventory_data()
        
        # Verifica se o resultado contém os dados esperados
        assert 'labels' in result
        assert 'datasets' in result
        assert len(result['datasets']) == 1
        assert result['datasets'][0]['data'] == [150, 75, 25]
        
        # Verifica se o método de banco de dados foi chamado
        mock_db.assert_called_once()

def test_get_tickets_data():
    """Testa se os dados de tickets são retornados corretamente."""
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_tickets_data_from_db') as mock_db:
        # Configura o mock para retornar dados de teste
        mock_db.return_value = {
            'labels': ['Alta', 'Média', 'Baixa'],
            'data': [3, 8, 12]
        }
        
        # Chama o método real que usa o mock internamente
        controller = DashboardController()
        result = controller.get_tickets_data()
        
        # Verifica se o resultado contém os dados esperados
        assert 'labels' in result
        assert 'datasets' in result
        assert len(result['datasets']) == 1
        assert result['datasets'][0]['data'] == [3, 8, 12]
        
        # Verifica se o método de banco de dados foi chamado
        mock_db.assert_called_once()

def test_apply_filters():
    """Testa se os filtros são aplicados corretamente aos dados."""
    controller = DashboardController()
    
    # Testa filtro de período
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_financial_data_from_db') as mock_db:
        controller.get_financial_data(period='last_month')
        # Verifica se o método foi chamado com o filtro correto
        mock_db.assert_called_once_with(period='last_month', department=None, status=None)
    
    # Testa filtro de departamento
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_sales_data_from_db') as mock_db:
        controller.get_sales_data(department='vendas')
        # Verifica se o método foi chamado com o filtro correto
        mock_db.assert_called_once_with(period=None, department='vendas', status=None)
    
    # Testa filtro de status
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_tickets_data_from_db') as mock_db:
        controller.get_tickets_data(status='aberto')
        # Verifica se o método foi chamado com o filtro correto
        mock_db.assert_called_once_with(period=None, department=None, status='aberto')
    
    # Testa múltiplos filtros
    with patch('app.dashboard.controllers.dashboard_controller.DashboardController._get_inventory_data_from_db') as mock_db:
        controller.get_inventory_data(period='last_quarter', department='estoque', status='ativo')
        # Verifica se o método foi chamado com todos os filtros
        mock_db.assert_called_once_with(period='last_quarter', department='estoque', status='ativo')
