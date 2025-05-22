#F:\Projetos_EasyData360\EasyERP\app\__init__.py
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.config import config_by_name
from app.extensions import db, migrate, jwt, ma
from app.shared.logging.config import configure_logging

# Blueprints Web
from app.core.routes import auth_routes, user_routes, profile_routes, user_interface_routes
from app.financeiro.routes import financeiro_routes
from app.vendas.controllers import cliente_controller, oportunidade_controller
from app.estoque.routes import estoque_routes
from app.dashboard import init_app as init_dashboard
from app.export import routes as export_routes

# Blueprints API RESTful (v1) - já são objetos Blueprint
from app.api.v1 import auth_api, financeiro_api, vendas_api, estoque_api


def create_app(env: str = "development") -> Flask:
    """
    Factory principal da aplicação Flask.
    Configura extensões, logging, rotas e tratamento de erros.
    """
    #app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__, instance_relative_config=True, template_folder="core/templates")
    app.config.from_object(config_by_name[env])

    # Configuração de logs centralizada
    configure_logging(app)

    # Inicialização das extensões principais
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    CORS(app)

    # Registro de rotas (Web e API)
    register_blueprints(app)

    # Tratamento global de exceções
    register_error_handlers(app)

    return app


def register_blueprints(app: Flask) -> None:
    """
    Registra todos os blueprints (Web e API RESTful) da aplicação.
    """
    try:
        # Blueprints Web
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(profile_routes.bp)
        app.register_blueprint(financeiro_routes.bp)
        app.register_blueprint(cliente_controller.bp)
        app.register_blueprint(oportunidade_controller.bp)
        app.register_blueprint(estoque_routes.bp)
        app.register_blueprint(user_interface_routes.user_interface)
        
        # Inicializa o módulo de dashboard
        init_dashboard(app)
        
        # Inicializa o módulo de exportação
        export_routes.init_app(app)

        # Blueprints API RESTful (v1) - diretamente os objetos Blueprint
        app.register_blueprint(auth_api, url_prefix="/api/v1")
        app.register_blueprint(financeiro_api, url_prefix="/api/v1")
        app.register_blueprint(vendas_api, url_prefix="/api/v1")
        app.register_blueprint(estoque_api, url_prefix="/api/v1")

        app.logger.info("Todos os blueprints foram registrados com sucesso.")

    except Exception as e:
        app.logger.exception("Erro ao registrar blueprints:")
        raise


def register_error_handlers(app: Flask) -> None:
    """
    Registra tratadores globais de erro para a aplicação.
    """
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        """
        Trata exceções HTTP padrão (404, 403, etc).
        """
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description
        }).data
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        """
        Trata exceções inesperadas (erro interno do servidor).
        """
        app.logger.exception("Erro inesperado")
        return jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "description": str(e)
        }), 500
