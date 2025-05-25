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
from app.core.models.user import User # Alterado de Usuario para User
from app.core.services.auth_service import registrar_login_sucesso, registrar_login_falha
from app.shared.utils.email_sender import send_confirmation_email # Importa função de envio

bp = Blueprint("auth", __name__, url_prefix="/auth")


# Login via FORMULÁRIO HTML
@bp.route("/login", methods=["GET", "POST"])
def login_form():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    senha = request.form.get("senha")

    user = User.query.filter_by(email=email).first() # Alterado para User

    if not user or not check_password_hash(user.senha_hash, senha):
        flash("Credenciais inválidas", "danger")
        registrar_login_falha(email)
        return render_template("login.html", error="E-mail ou senha incorretos.")

    if not user.ativo:
        flash("Usuário inativo.", "warning")
        return render_template("login.html", error="Usuário inativo.")
        
    # Verifica se o e-mail foi confirmado
    if not user.email_confirmed:
        flash("Seu e-mail ainda não foi confirmado. Verifique sua caixa de entrada.", "warning")
        # Opcional: oferecer reenvio do e-mail de confirmação
        # send_confirmation_email(user) # Cuidado com abuso
        return render_template("login.html", error="E-mail não confirmado.")

    registrar_login_sucesso(user)
    flash("Login realizado com sucesso!", "success")
    # TODO: Implementar sessão de usuário real aqui (Flask-Login ou similar)
    # Por enquanto, redireciona para uma página genérica
    return redirect(url_for("user_interface.dashboard")) # Redirecionar para dashboard ou perfil


# Cadastro via FORMULÁRIO HTML
@bp.route("/register", methods=["GET", "POST"])
def register_form():
    if request.method == "GET":
        # Opcional: buscar perfis e supervisores do banco
        # perfis = Perfil.query.all() # Modelo Perfil precisa existir
        # supervisores = User.query.filter_by(ativo=True).all()
        perfis = [] # Placeholder
        supervisores = [] # Placeholder
        return render_template("register.html", perfis=perfis, supervisores=supervisores)

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    # perfil_id = request.form.get("perfil_id") # Assumindo que Perfil existe e tem ID integer
    # supervisor_id = request.form.get("supervisor_id") or None
    perfil_id = 1 # Placeholder - Assumindo que existe um perfil com ID 1
    supervisor_id = None # Placeholder

    if User.query.filter_by(email=email).first():
        flash("E-mail já cadastrado.", "warning")
        return render_template("register.html", error="E-mail já cadastrado.")

    user = User(
        nome=nome,
        email=email,
        senha_hash=generate_password_hash(senha),
        perfil_id=perfil_id, # Usar o ID real do perfil
        supervisor_id=supervisor_id,
        ativo=True, # Usuário começa ativo, mas não confirmado
        email_confirmed=False
    )
    db.session.add(user)
    db.session.commit()
    
    # Envia o e-mail de confirmação
    try:
        send_confirmation_email(user)
        flash("Cadastro realizado com sucesso! Um e-mail de confirmação foi enviado.", "success")
    except Exception as e:
        current_app.logger.error(f"Falha ao enviar e-mail de confirmação para {email}: {e}")
        flash("Cadastro realizado, mas houve um erro ao enviar o e-mail de confirmação. Contate o suporte.", "warning")
        # Considerar rollback ou marcar usuário para reenvio?
        
    return redirect(url_for("auth.login_form"))

# Rota para confirmar o e-mail via token
@bp.route("/confirm/<token>")
def confirm_email(token):
    user = User.query.filter_by(confirmation_token=token).first()
    if user:
        if user.confirm_email(token):
            db.session.commit()
            flash("Seu e-mail foi confirmado com sucesso! Você já pode fazer login.", "success")
        else:
            flash("O link de confirmação é inválido ou expirou.", "danger")
    else:
        flash("Link de confirmação inválido.", "danger")
        
    return redirect(url_for("auth.login_form"))


# Login via API JSON
@bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first() # Alterado para User

    if not user or not check_password_hash(user.senha_hash, senha):
        registrar_login_falha(email)
        return jsonify({"erro": "Credenciais inválidas"}), 401

    if not user.ativo:
        return jsonify({"erro": "Usuário inativo"}), 403
        
    # Verifica confirmação de e-mail para API também
    if not user.email_confirmed:
        return jsonify({"erro": "E-mail não confirmado"}), 403

    access_token = create_access_token(identity=user.id) # Usa ID inteiro
    refresh_token = create_refresh_token(identity=user.id)
    registrar_login_sucesso(user)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "usuario": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "perfil": user.perfil.nome if user.perfil else None
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
    user = User.query.get(usuario_id) # Alterado para User

    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "perfil": user.perfil.nome if user.perfil else None,
        "ativo": user.ativo,
        "email_confirmed": user.email_confirmed
    })
