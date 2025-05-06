# app/financeiro/routes/financeiro_routes.py

from flask import Blueprint
from app.financeiro.controllers.account_controller import bp as contas_bp
from app.financeiro.controllers.transaction_controller import bp as lancamentos_bp

bp = Blueprint("financeiro", __name__)

# Agrupa e registra os blueprints específicos
bp.register_blueprint(contas_bp, url_prefix="/financeiro/contas")
bp.register_blueprint(lancamentos_bp, url_prefix="/financeiro/lancamentos")
