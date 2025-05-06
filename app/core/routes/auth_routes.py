# app/core/routes/auth_routes.py

from app.core.controllers.auth_controller import bp as auth_bp

# Blueprint da autenticação (login, refresh, me)
bp = auth_bp
