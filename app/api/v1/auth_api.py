# app/api/v1/auth_api.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.core.models.user import Usuario
from app.extensions import db
from werkzeug.security import check_password_hash

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    email = dados.get("email")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"erro": "E-mail e senha são obrigatórios."}), 400

    usuario = Usuario.query.filter_by(email=email, ativo=True).first()
    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({"erro": "Credenciais inválidas."}), 401

    access_token = create_access_token(identity=str(usuario.id))
    return jsonify({
        "access_token": access_token,
        "usuario": {
            "id": str(usuario.id),
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil_id": str(usuario.perfil_id)
        }
    }), 200


@auth_api.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(user_id)

    return jsonify({
        "id": str(usuario.id),
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil_id": str(usuario.perfil_id),
        "ativo": usuario.ativo,
        "criado_em": usuario.criado_em.isoformat()
    }), 200


@auth_api.route("/check", methods=["GET"])
@jwt_required()
def check_token():
    return jsonify({"status": "válido"}), 200
