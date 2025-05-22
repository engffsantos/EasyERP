from flask import Blueprint, request, Response, send_file
import csv
import io
import pandas as pd
from datetime import datetime

# Blueprint para exportação de dados
export_bp = Blueprint('export', __name__, url_prefix='/export')

def generate_csv(data, filename):
    """
    Gera um arquivo CSV a partir dos dados fornecidos
    
    Args:
        data: Lista de dicionários com os dados a serem exportados
        filename: Nome do arquivo a ser gerado
        
    Returns:
        Objeto Response com o arquivo CSV para download
    """
    si = io.StringIO()
    if not data:
        si.write("Nenhum dado encontrado")
    else:
        writer = csv.DictWriter(si, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    output = si.getvalue()
    si.close()
    
    response = Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )
    
    return response

def generate_excel(data, filename):
    """
    Gera um arquivo Excel a partir dos dados fornecidos
    
    Args:
        data: Lista de dicionários com os dados a serem exportados
        filename: Nome do arquivo a ser gerado
        
    Returns:
        Objeto Response com o arquivo Excel para download
    """
    output = io.BytesIO()
    
    if not data:
        # Criar um DataFrame vazio com mensagem
        df = pd.DataFrame([{"Mensagem": "Nenhum dado encontrado"}])
    else:
        df = pd.DataFrame(data)
    
    # Criar um objeto ExcelWriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Dados', index=False)
        
        # Ajustar largura das colunas
        worksheet = writer.sheets['Dados']
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename
    )

# Função auxiliar para obter dados simulados do módulo financeiro
def get_financeiro_data():
    """Retorna dados simulados do módulo financeiro"""
    return [
        {
            "id": 1,
            "data": "2025-01-15",
            "tipo": "Receita",
            "categoria": "Vendas",
            "descricao": "Venda de produtos",
            "valor": 5000.00,
            "status": "Confirmado"
        },
        {
            "id": 2,
            "data": "2025-01-20",
            "tipo": "Despesa",
            "categoria": "Fornecedores",
            "descricao": "Pagamento de insumos",
            "valor": 2500.00,
            "status": "Confirmado"
        },
        {
            "id": 3,
            "data": "2025-02-05",
            "tipo": "Receita",
            "categoria": "Serviços",
            "descricao": "Consultoria",
            "valor": 3000.00,
            "status": "Pendente"
        },
        {
            "id": 4,
            "data": "2025-02-10",
            "tipo": "Despesa",
            "categoria": "Operacional",
            "descricao": "Aluguel",
            "valor": 1800.00,
            "status": "Confirmado"
        },
        {
            "id": 5,
            "data": "2025-03-01",
            "tipo": "Despesa",
            "categoria": "Impostos",
            "descricao": "Impostos mensais",
            "valor": 1200.00,
            "status": "Pendente"
        }
    ]

# Função auxiliar para obter dados simulados do módulo vendas
def get_vendas_data():
    """Retorna dados simulados do módulo vendas"""
    return [
        {
            "id": 1,
            "cliente": "Empresa ABC Ltda",
            "data": "2025-01-10",
            "produto": "Software ERP",
            "quantidade": 1,
            "valor_unitario": 12000.00,
            "valor_total": 12000.00,
            "status": "Fechado"
        },
        {
            "id": 2,
            "cliente": "Comércio XYZ",
            "data": "2025-01-15",
            "produto": "Módulo Financeiro",
            "quantidade": 1,
            "valor_unitario": 3000.00,
            "valor_total": 3000.00,
            "status": "Negociação"
        },
        {
            "id": 3,
            "cliente": "Indústria 123",
            "data": "2025-02-01",
            "produto": "Módulo Estoque",
            "quantidade": 1,
            "valor_unitario": 2500.00,
            "valor_total": 2500.00,
            "status": "Proposta"
        },
        {
            "id": 4,
            "cliente": "Consultoria DEF",
            "data": "2025-02-20",
            "produto": "Suporte Premium",
            "quantidade": 12,
            "valor_unitario": 500.00,
            "valor_total": 6000.00,
            "status": "Fechado"
        },
        {
            "id": 5,
            "cliente": "Varejo QWE",
            "data": "2025-03-05",
            "produto": "Treinamento",
            "quantidade": 5,
            "valor_unitario": 800.00,
            "valor_total": 4000.00,
            "status": "Prospectando"
        }
    ]

# Função auxiliar para obter dados simulados do módulo estoque
def get_estoque_data():
    """Retorna dados simulados do módulo estoque"""
    return [
        {
            "id": 1,
            "produto": "Notebook Dell",
            "categoria": "Equipamentos",
            "quantidade": 15,
            "valor_unitario": 4500.00,
            "valor_total": 67500.00,
            "fornecedor": "Dell Computadores",
            "data_ultima_compra": "2025-01-05"
        },
        {
            "id": 2,
            "produto": "Monitor 24\"",
            "categoria": "Equipamentos",
            "quantidade": 30,
            "valor_unitario": 1200.00,
            "valor_total": 36000.00,
            "fornecedor": "LG Eletrônicos",
            "data_ultima_compra": "2025-01-10"
        },
        {
            "id": 3,
            "produto": "Teclado sem fio",
            "categoria": "Periféricos",
            "quantidade": 50,
            "valor_unitario": 150.00,
            "valor_total": 7500.00,
            "fornecedor": "Logitech",
            "data_ultima_compra": "2025-01-15"
        },
        {
            "id": 4,
            "produto": "Mouse óptico",
            "categoria": "Periféricos",
            "quantidade": 60,
            "valor_unitario": 80.00,
            "valor_total": 4800.00,
            "fornecedor": "Logitech",
            "data_ultima_compra": "2025-01-15"
        },
        {
            "id": 5,
            "produto": "Servidor Rack",
            "categoria": "Infraestrutura",
            "quantidade": 3,
            "valor_unitario": 15000.00,
            "valor_total": 45000.00,
            "fornecedor": "Dell Computadores",
            "data_ultima_compra": "2025-02-01"
        }
    ]

# Função auxiliar para obter dados simulados do módulo service desk
def get_service_desk_data():
    """Retorna dados simulados do módulo service desk"""
    return [
        {
            "id": 1,
            "titulo": "Sistema lento",
            "descricao": "O sistema está respondendo com lentidão",
            "solicitante": "João Silva",
            "departamento": "Financeiro",
            "prioridade": "Alta",
            "status": "Aberto",
            "data_abertura": "2025-01-10",
            "data_resolucao": None
        },
        {
            "id": 2,
            "titulo": "Erro ao gerar relatório",
            "descricao": "Erro 500 ao tentar gerar relatório mensal",
            "solicitante": "Maria Oliveira",
            "departamento": "Vendas",
            "prioridade": "Média",
            "status": "Em andamento",
            "data_abertura": "2025-01-15",
            "data_resolucao": None
        },
        {
            "id": 3,
            "titulo": "Solicitação de novo usuário",
            "descricao": "Criar acesso para novo funcionário",
            "solicitante": "Carlos Pereira",
            "departamento": "RH",
            "prioridade": "Baixa",
            "status": "Resolvido",
            "data_abertura": "2025-01-20",
            "data_resolucao": "2025-01-21"
        },
        {
            "id": 4,
            "titulo": "Sistema indisponível",
            "descricao": "Não consigo acessar o sistema",
            "solicitante": "Ana Souza",
            "departamento": "Estoque",
            "prioridade": "Crítica",
            "status": "Resolvido",
            "data_abertura": "2025-02-01",
            "data_resolucao": "2025-02-01"
        },
        {
            "id": 5,
            "titulo": "Atualização de cadastro",
            "descricao": "Preciso atualizar informações de cliente",
            "solicitante": "Paulo Santos",
            "departamento": "Vendas",
            "prioridade": "Baixa",
            "status": "Aberto",
            "data_abertura": "2025-02-10",
            "data_resolucao": None
        }
    ]

# Rotas para exportação de dados do módulo financeiro
@export_bp.route('/financeiro', methods=['GET'])
def export_financeiro():
    """Exporta dados do módulo financeiro"""
    format_type = request.args.get('format', 'csv')
    data = get_financeiro_data()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == 'excel':
        return generate_excel(data, f"financeiro_{timestamp}.xlsx")
    else:
        return generate_csv(data, f"financeiro_{timestamp}.csv")

# Rotas para exportação de dados do módulo vendas
@export_bp.route('/vendas', methods=['GET'])
def export_vendas():
    """Exporta dados do módulo vendas"""
    format_type = request.args.get('format', 'csv')
    data = get_vendas_data()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == 'excel':
        return generate_excel(data, f"vendas_{timestamp}.xlsx")
    else:
        return generate_csv(data, f"vendas_{timestamp}.csv")

# Rotas para exportação de dados do módulo estoque
@export_bp.route('/estoque', methods=['GET'])
def export_estoque():
    """Exporta dados do módulo estoque"""
    format_type = request.args.get('format', 'csv')
    data = get_estoque_data()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == 'excel':
        return generate_excel(data, f"estoque_{timestamp}.xlsx")
    else:
        return generate_csv(data, f"estoque_{timestamp}.csv")

# Rotas para exportação de dados do módulo service desk
@export_bp.route('/service_desk', methods=['GET'])
def export_service_desk():
    """Exporta dados do módulo service desk"""
    format_type = request.args.get('format', 'csv')
    data = get_service_desk_data()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == 'excel':
        return generate_excel(data, f"service_desk_{timestamp}.xlsx")
    else:
        return generate_csv(data, f"service_desk_{timestamp}.csv")
