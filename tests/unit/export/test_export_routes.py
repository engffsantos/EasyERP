import pytest
from unittest.mock import patch, MagicMock
import io
import csv
import pandas as pd

def test_export_page_renders(client):
    """Testa se a página de exportação é renderizada corretamente."""
    response = client.get('/export/')
    assert response.status_code == 200
    assert b'Exportar Dados' in response.data
    assert b'Financeiro' in response.data
    assert b'Vendas' in response.data
    assert b'Estoque' in response.data
    assert b'Service Desk' in response.data

def test_export_csv_financial(client):
    """Testa a exportação de dados financeiros em CSV."""
    with patch('app.export.routes.get_financial_data') as mock_get_data:
        # Configura o mock para retornar dados de teste
        mock_data = [
            {'id': 1, 'data': '2023-01-01', 'descricao': 'Venda', 'valor': 1000.0, 'tipo': 'receita'},
            {'id': 2, 'data': '2023-01-02', 'descricao': 'Aluguel', 'valor': 800.0, 'tipo': 'despesa'}
        ]
        mock_get_data.return_value = mock_data
        
        # Faz a requisição para exportar
        response = client.get('/export/financial/csv')
        
        # Verifica se a resposta é um arquivo CSV
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
        assert 'attachment; filename=' in response.headers['Content-Disposition']
        
        # Verifica o conteúdo do CSV
        content = response.data.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        
        # Verifica o cabeçalho e os dados
        assert rows[0] == ['id', 'data', 'descricao', 'valor', 'tipo']
        assert rows[1] == ['1', '2023-01-01', 'Venda', '1000.0', 'receita']
        assert rows[2] == ['2', '2023-01-02', 'Aluguel', '800.0', 'despesa']

def test_export_excel_sales(client):
    """Testa a exportação de dados de vendas em Excel."""
    with patch('app.export.routes.get_sales_data') as mock_get_data:
        # Configura o mock para retornar dados de teste
        mock_data = [
            {'id': 1, 'cliente': 'Empresa A', 'produto': 'Serviço X', 'valor': 5000.0, 'status': 'Ganho'},
            {'id': 2, 'cliente': 'Empresa B', 'produto': 'Serviço Y', 'valor': 3000.0, 'status': 'Em andamento'}
        ]
        mock_get_data.return_value = mock_data
        
        # Mock para o pandas ExcelWriter
        mock_excel_writer = MagicMock()
        with patch('pandas.ExcelWriter', return_value=mock_excel_writer):
            with patch('pandas.DataFrame') as mock_df:
                # Configura o mock do DataFrame
                mock_df_instance = MagicMock()
                mock_df.return_value = mock_df_instance
                
                # Faz a requisição para exportar
                response = client.get('/export/sales/excel')
                
                # Verifica se a resposta é um arquivo Excel
                assert response.status_code == 200
                assert response.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                assert 'attachment; filename=' in response.headers['Content-Disposition']
                
                # Verifica se o DataFrame foi criado com os dados corretos
                mock_df.assert_called_once()
                args, kwargs = mock_df.call_args
                assert kwargs['data'] == mock_data
                
                # Verifica se o método to_excel foi chamado
                mock_df_instance.to_excel.assert_called_once()

def test_export_invalid_module(client):
    """Testa a exportação com um módulo inválido."""
    response = client.get('/export/invalid_module/csv')
    assert response.status_code == 404

def test_export_invalid_format(client):
    """Testa a exportação com um formato inválido."""
    response = client.get('/export/financial/invalid_format')
    assert response.status_code == 400
    assert b'Formato de exporta\xc3\xa7\xc3\xa3o inv\xc3\xa1lido' in response.data
