# app/estoque/routes/estoque_routes.py

from flask import Blueprint
from app.estoque.controllers.estoque_controller import bp as estoque_controller_bp

bp = Blueprint("estoque", __name__)

# Registra os sub-blueprints específicos
bp.register_blueprint(estoque_controller_bp, url_prefix="/estoque")
