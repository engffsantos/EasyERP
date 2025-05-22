from app.dashboard.routes.dashboard_routes import dashboard_bp

def init_app(app):
    """Inicializa o módulo de dashboard na aplicação Flask"""
    app.register_blueprint(dashboard_bp)
