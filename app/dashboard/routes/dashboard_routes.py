from flask import Blueprint
from app.dashboard.controllers.dashboard_controller import DashboardController

# Criação do blueprint para o módulo de dashboard
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Rota principal do dashboard
dashboard_bp.route('/', methods=['GET'])(DashboardController.render_dashboard)

# Rotas para API de dados dos gráficos
dashboard_bp.route('/api/financial', methods=['GET'])(DashboardController.get_financial_data)
dashboard_bp.route('/api/sales', methods=['GET'])(DashboardController.get_sales_data)
dashboard_bp.route('/api/inventory', methods=['GET'])(DashboardController.get_inventory_data)
dashboard_bp.route('/api/tickets', methods=['GET'])(DashboardController.get_tickets_data)
