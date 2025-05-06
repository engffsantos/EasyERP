# app/api/v1/__init__.py

from flask import Blueprint
from app.api.v1.auth_api import auth_api
from app.api.v1.financeiro_api import financeiro_api
from app.api.v1.vendas_api import vendas_api
from app.api.v1.estoque_api import estoque_api

# Define o blueprint principal da API v1
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Registra os sub-blueprints dos módulos específicos
api_v1.register_blueprint(auth_api)
api_v1.register_blueprint(financeiro_api)
api_v1.register_blueprint(vendas_api)
api_v1.register_blueprint(estoque_api)
