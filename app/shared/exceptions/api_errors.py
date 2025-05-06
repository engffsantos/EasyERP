# app/shared/exceptions/api_errors.py

from flask import jsonify
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, InternalServerError
from app.shared.exceptions.business_rules import RegraNegocioException


def registrar_tratadores_de_erros(app):
    """
    Registra tratadores globais de erro para a aplicação Flask.
    """

    @app.errorhandler(RegraNegocioException)
    def tratar_erro_regra_negocio(e):
        response = jsonify(e.to_dict())
        response.status_code = 422
        return response

    @app.errorhandler(NotFound)
    def tratar_erro_nao_encontrado(e):
        return jsonify({
            "erro": "nao_encontrado",
            "mensagem": "Recurso não encontrado."
        }), 404

    @app.errorhandler(BadRequest)
    def tratar_erro_requisicao_invalida(e):
        return jsonify({
            "erro": "requisicao_invalida",
            "mensagem": "A requisição está malformada ou possui dados inválidos."
        }), 400

    @app.errorhandler(HTTPException)
    def tratar_http_exception(e):
        return jsonify({
            "erro": e.name.lower().replace(" ", "_"),
            "mensagem": e.description
        }), e.code

    @app.errorhandler(Exception)
    def tratar_erro_interno(e):
        # Log real pode ser incluído aqui
        return jsonify({
            "erro": "erro_interno",
            "mensagem": "Ocorreu um erro inesperado no servidor."
        }), 500
