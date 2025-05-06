# app/core/controllers/auth_controller.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.core.models.user import Usuario
from app.core.services.auth_service import registrar_login_sucesso, registrar_login_falha

bp = Blueprint("auth", __name__, url_prefix="/auth")


# Login via FORMULÁRIO HTML
@bp.route("/login", methods=["GET", "POST"])
def login_form():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        flash("Credenciais inválidas", "danger")
        registrar_login_falha(email)
        return render_template("login.html", error="E-mail ou senha incorretos.")

    if not usuario.ativo:
        return render_template("login.html", error="Usuário inativo.")

    registrar_login_sucesso(usuario)
    flash("Login realizado com sucesso!", "success")
    return redirect(url_for("user_interface.criar_usuario"))  # ou outra rota pós-login


# Cadastro via FORMULÁRIO HTML
@bp.route("/register", methods=["GET", "POST"])
def register_form():
    if request.method == "GET":
        # Opcional: buscar perfis e supervisores do banco
        perfis = Usuario.query.all()  # Substitua por query real de Perfil
        supervisores = Usuario.query.all()  # Substitua por query real de Supervisores
        return render_template("register.html", perfis=perfis, supervisores=supervisores)

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    perfil_id = request.form.get("perfil_id")
    supervisor_id = request.form.get("supervisor_id") or None

    if Usuario.query.filter_by(email=email).first():
        return render_template("register.html", error="E-mail já cadastrado.")

    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=generate_password_hash(senha),
        perfil_id=perfil_id,
        supervisor_id=supervisor_id,
        ativo=True
    )
    db.session.add(usuario)
    db.session.commit()
    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for("auth.login_form"))


# Login via API JSON
@bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        registrar_login_falha(email)
        return jsonify({"erro": "Credenciais inválidas"}), 401

    if not usuario.ativo:
        return jsonify({"erro": "Usuário inativo"}), 403

    access_token = create_access_token(identity=str(usuario.id))
    refresh_token = create_refresh_token(identity=str(usuario.id))
    registrar_login_sucesso(usuario)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "usuario": {
            "id": str(usuario.id),
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil.nome if usuario.perfil else None
        }
    })


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    usuario_id = get_jwt_identity()
    novo_token = create_access_token(identity=usuario_id)
    return jsonify({"access_token": novo_token})


@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": str(usuario.id),
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil.nome if usuario.perfil else None,
        "ativo": usuario.ativo
    })
