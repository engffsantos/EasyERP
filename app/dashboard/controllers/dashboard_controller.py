from flask import render_template, jsonify, request
from app.financeiro.models.transaction import Transaction
from app.vendas.models.oportunidade import Oportunidade
from app.estoque.models.inventory import Inventory
from app.service_desk.models.ticket import Ticket
from sqlalchemy import func
from datetime import datetime, timedelta
import random

class DashboardController:
    """
    Controlador para o Dashboard de BI
    Responsável por fornecer dados para os gráficos e visualizações
    """
    
    @staticmethod
    def render_dashboard():
        """Renderiza a página principal do dashboard"""
        return render_template('dashboard/index.html')
    
    @staticmethod
    def get_financial_data():
        """Retorna dados financeiros para gráficos com suporte a filtros"""
        # Obter parâmetros de filtro
        period = request.args.get('period', 'semester')
        profile = request.args.get('profile', 'all')
        status = request.args.get('status', 'all')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Determinar o período de dados com base no filtro
        today = datetime.now()
        num_months = 6  # Padrão: semestre
        
        if period == 'month':
            num_months = 1
        elif period == 'quarter':
            num_months = 3
        elif period == 'year':
            num_months = 12
        elif period == 'custom' and start_date and end_date:
            # Período personalizado - implementação simplificada
            # Em produção, usaria as datas reais para filtrar
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                delta = end - start
                num_months = max(1, round(delta.days / 30))
            except ValueError:
                num_months = 6  # Fallback para semestre
        
        # Gerar dados para o período selecionado
        months = []
        revenues = []
        expenses = []
        
        for i in range(num_months - 1, -1, -1):
            # Calcula o mês
            month_date = today - timedelta(days=30 * i)
            month_name = month_date.strftime('%b')
            months.append(month_name)
            
            # Simulação de dados com variação baseada nos filtros
            base_revenue = random.randint(50000, 150000)
            base_expense = random.randint(30000, 100000)
            
            # Aplicar modificadores baseados no perfil selecionado
            if profile == 'financeiro':
                base_revenue *= 1.2
                base_expense *= 0.9
            elif profile == 'vendas':
                base_revenue *= 1.5
                base_expense *= 1.1
            elif profile == 'estoque':
                base_revenue *= 0.8
                base_expense *= 1.3
            elif profile == 'ti':
                base_revenue *= 0.7
                base_expense *= 1.2
            
            # Aplicar modificadores baseados no status selecionado
            if status == 'active':
                base_revenue *= 1.2
                base_expense *= 0.9
            elif status == 'pending':
                base_revenue *= 0.8
                base_expense *= 1.1
            elif status == 'completed':
                base_revenue *= 1.3
                base_expense *= 0.8
            elif status == 'canceled':
                base_revenue *= 0.5
                base_expense *= 0.7
            
            revenues.append(int(base_revenue))
            expenses.append(int(base_expense))
        
        return jsonify({
            'labels': months,
            'datasets': [
                {
                    'label': 'Receitas',
                    'data': revenues,
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1
                },
                {
                    'label': 'Despesas',
                    'data': expenses,
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 1
                }
            ]
        })
    
    @staticmethod
    def get_sales_data():
        """Retorna dados de vendas para gráficos com suporte a filtros"""
        # Obter parâmetros de filtro
        period = request.args.get('period', 'semester')
        profile = request.args.get('profile', 'all')
        status = request.args.get('status', 'all')
        
        # Dados base para o gráfico de vendas (por status)
        statuses = ['Prospectando', 'Proposta', 'Negociação', 'Fechado', 'Perdido']
        base_counts = [15, 8, 5, 12, 3]  # Contagens base
        
        # Aplicar modificadores baseados no período
        period_modifier = 1.0
        if period == 'month':
            period_modifier = 0.5
        elif period == 'quarter':
            period_modifier = 0.8
        elif period == 'year':
            period_modifier = 1.5
        
        # Aplicar modificadores baseados no perfil
        profile_modifiers = {
            'all': [1.0, 1.0, 1.0, 1.0, 1.0],
            'financeiro': [0.7, 0.8, 0.9, 1.2, 0.6],
            'vendas': [1.5, 1.3, 1.2, 1.4, 0.8],
            'estoque': [0.8, 0.9, 1.0, 1.1, 0.7],
            'ti': [0.6, 0.7, 0.8, 0.9, 1.0]
        }
        
        # Aplicar modificadores baseados no status
        status_modifiers = {
            'all': [1.0, 1.0, 1.0, 1.0, 1.0],
            'active': [1.2, 1.3, 1.4, 0.8, 0.5],
            'pending': [1.5, 1.2, 0.9, 0.6, 0.3],
            'completed': [0.5, 0.6, 0.7, 1.8, 0.4],
            'canceled': [0.3, 0.4, 0.5, 0.6, 1.7]
        }
        
        # Calcular contagens finais com os modificadores
        counts = []
        for i in range(len(base_counts)):
            # Aplicar todos os modificadores
            modified_count = base_counts[i] * period_modifier
            modified_count *= profile_modifiers.get(profile, profile_modifiers['all'])[i]
            modified_count *= status_modifiers.get(status, status_modifiers['all'])[i]
            counts.append(int(modified_count))
        
        return jsonify({
            'labels': statuses,
            'datasets': [{
                'label': 'Oportunidades por Status',
                'data': counts,
                'backgroundColor': [
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 99, 132, 0.5)'
                ],
                'borderWidth': 1
            }]
        })
    
    @staticmethod
    def get_inventory_data():
        """Retorna dados de estoque para gráficos com suporte a filtros"""
        # Obter parâmetros de filtro
        period = request.args.get('period', 'semester')
        profile = request.args.get('profile', 'all')
        status = request.args.get('status', 'all')
        
        # Dados base para o gráfico de estoque (top 5 produtos)
        products = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
        base_quantities = [120, 85, 65, 45, 30]  # Quantidades base
        
        # Aplicar modificadores baseados no período
        period_modifier = 1.0
        if period == 'month':
            period_modifier = 0.7
        elif period == 'quarter':
            period_modifier = 0.9
        elif period == 'year':
            period_modifier = 1.3
        
        # Aplicar modificadores baseados no perfil
        profile_modifiers = {
            'all': [1.0, 1.0, 1.0, 1.0, 1.0],
            'financeiro': [0.8, 0.8, 0.8, 0.8, 0.8],
            'vendas': [0.9, 0.9, 0.9, 0.9, 0.9],
            'estoque': [1.5, 1.4, 1.3, 1.2, 1.1],
            'ti': [0.7, 0.7, 0.7, 0.7, 0.7]
        }
        
        # Aplicar modificadores baseados no status
        status_modifiers = {
            'all': [1.0, 1.0, 1.0, 1.0, 1.0],
            'active': [1.2, 1.1, 1.0, 0.9, 0.8],
            'pending': [0.8, 0.9, 1.0, 1.1, 1.2],
            'completed': [1.0, 1.0, 1.0, 1.0, 1.0],
            'canceled': [0.5, 0.6, 0.7, 0.8, 0.9]
        }
        
        # Calcular quantidades finais com os modificadores
        quantities = []
        for i in range(len(base_quantities)):
            # Aplicar todos os modificadores
            modified_quantity = base_quantities[i] * period_modifier
            modified_quantity *= profile_modifiers.get(profile, profile_modifiers['all'])[i]
            modified_quantity *= status_modifiers.get(status, status_modifiers['all'])[i]
            quantities.append(int(modified_quantity))
        
        return jsonify({
            'labels': products,
            'datasets': [{
                'label': 'Quantidade em Estoque',
                'data': quantities,
                'backgroundColor': 'rgba(153, 102, 255, 0.5)',
                'borderColor': 'rgba(153, 102, 255, 1)',
                'borderWidth': 1
            }]
        })
    
    @staticmethod
    def get_tickets_data():
        """Retorna dados de tickets para gráficos com suporte a filtros"""
        # Obter parâmetros de filtro
        period = request.args.get('period', 'semester')
        profile = request.args.get('profile', 'all')
        status = request.args.get('status', 'all')
        
        # Dados base para o gráfico de tickets (por prioridade)
        priorities = ['Baixa', 'Média', 'Alta', 'Crítica']
        base_counts = [25, 18, 12, 5]  # Contagens base
        
        # Aplicar modificadores baseados no período
        period_modifier = 1.0
        if period == 'month':
            period_modifier = 0.6
        elif period == 'quarter':
            period_modifier = 0.8
        elif period == 'year':
            period_modifier = 1.4
        
        # Aplicar modificadores baseados no perfil
        profile_modifiers = {
            'all': [1.0, 1.0, 1.0, 1.0],
            'financeiro': [0.7, 0.8, 0.9, 0.5],
            'vendas': [0.8, 0.9, 0.7, 0.6],
            'estoque': [0.9, 0.8, 0.7, 0.6],
            'ti': [1.5, 1.4, 1.3, 1.2]
        }
        
        # Aplicar modificadores baseados no status
        status_modifiers = {
            'all': [1.0, 1.0, 1.0, 1.0],
            'active': [0.8, 1.2, 1.5, 1.8],
            'pending': [1.2, 1.5, 1.2, 0.8],
            'completed': [1.5, 0.8, 0.5, 0.3],
            'canceled': [0.5, 0.4, 0.3, 0.2]
        }
        
        # Calcular contagens finais com os modificadores
        counts = []
        for i in range(len(base_counts)):
            # Aplicar todos os modificadores
            modified_count = base_counts[i] * period_modifier
            modified_count *= profile_modifiers.get(profile, profile_modifiers['all'])[i]
            modified_count *= status_modifiers.get(status, status_modifiers['all'])[i]
            counts.append(int(modified_count))
        
        return jsonify({
            'labels': priorities,
            'datasets': [{
                'label': 'Tickets por Prioridade',
                'data': counts,
                'backgroundColor': [
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                    'rgba(255, 99, 132, 0.5)'
                ],
                'borderWidth': 1
            }]
        })
