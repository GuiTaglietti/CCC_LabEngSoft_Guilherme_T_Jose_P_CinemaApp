import string
import secrets
from server import get_db
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, decode_token
from app.util.util import verify_password, hash_password, _mailgun_send
from server import get_db
from datetime import timedelta
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user or not verify_password(user['password'], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"user_id": user['id'], "username": user['username'], "role": user['role']})
    return jsonify({
        "access_token": access_token,
        "role": user['role']
    }), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    fullname = data.get("fullname")
    cpf = data.get("cpf")
    email = data.get("email")
    confirm_email = data.get("confirmEmail")
    username = data.get("username")
    password = data.get("password")

    if email != confirm_email:
        return jsonify({"msg": "Email de confirmação não corresponde!"}), 400

    cursor = get_db()

    cursor.execute("SELECT 1 FROM users WHERE cpf = %s", (cpf,))
    if cursor.fetchone():
        return jsonify({"msg": "CPF já cadastrado!"}), 400

    cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"msg": "Email já cadastrado!"}), 400

    cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({"msg": "Nome de usuário já cadastrado!"}), 400

    hashed_password = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password, fullname, email, cpf, role)
        VALUES (%s, %s, %s, %s, %s, 'usuario')
    """, (username, hashed_password, fullname, email, cpf))
    cursor.connection.commit()

    return jsonify({"msg": "Usuário cadastrado com sucesso!"}), 201

@auth_bp.route("/users/update", methods=["PUT"])
def update_user():
    data = request.json
    username = data.get("username")
    full_name = data.get("full_name")
    email = data.get("email")

    if not username or not full_name or not email:
        return jsonify({"msg": "Campos obrigatórios faltando."}), 400

    cursor = get_db()
    cursor.execute("""
        UPDATE users SET fullname = %s, email = %s
        WHERE username = %s
    """, (full_name, email, username))
    cursor.connection.commit()

    return jsonify({"msg": "Dados atualizados com sucesso."}), 200


@auth_bp.route("/users/me", methods=["GET"])
def get_user_info():
    username = request.args.get("username")

    if not username:
        return jsonify({"msg": "Username é obrigatório."}), 400

    cursor = get_db()
    cursor.execute("SELECT username, fullname, email FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"msg": "Usuário não encontrado."}), 404

    return jsonify({
        "username": user["username"],
        "full_name": user["fullname"],
        "email": user["email"]
    }), 200


def generate_password(tamanho=12):
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alfabeto) for _ in range(tamanho))


@auth_bp.route("/send-reset-link", methods=["POST"])
def send_reset_link():
    data = request.json
    email = data.get("email")
    if not email:
        return jsonify({"msg": "E-mail é obrigatório."}), 400

    cursor = get_db()
    cursor.execute("SELECT id, username FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"msg": "E-mail não encontrado."}), 404

    expires = timedelta(minutes=15)
    reset_token = create_access_token(
        identity={"user_id": user["id"], "username": user["username"]},
        expires_delta=expires,
    )

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"

    subject = "Cinema: Redefinição de Senha"
    text = (
        f"Olá, {user['username']},\n\n"
        "Você solicitou a redefinição de senha. Clique no link abaixo para criar uma nova senha:\n\n"
        f"{reset_link}\n\n"
        "Este link expira em 15 minutos.\n\n"
        "Se você não solicitou esta ação, desconsidere este e-mail.\n\n"
        "Atenciosamente,\nEquipe Cinema"
    )

    sucesso = _mailgun_send(subject, text)
    if not sucesso:
        return jsonify({"msg": "Falha ao enviar e-mail de redefinição."}), 500

    return jsonify({"msg": "E-mail de redefinição enviado com sucesso."}), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"msg": "Token e nova senha são obrigatórios."}), 400

    try:
        decoded = decode_token(token)
    except:
        return jsonify({"msg": "Token inválido ou expirado."}), 400

    identity = decoded.get("sub") or decoded.get("identity")
    user_id = identity.get("user_id")
    hashed = hash_password(new_password)
    cursor = get_db()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
    cursor.connection.commit()

    return jsonify({"msg": "Senha alterada com sucesso."}), 200

@auth_bp.route("/send-maintenance", methods=["POST"])
def send_maintenance():
    data = request.json
    sender_name = data.get("sender")
    content = data.get("content")

    if not sender_name or not content:
        return jsonify({"msg": "Remetente e conteúdo são obrigatórios."}), 400

    subject = "Cinema: Notificação de Manutenção"
    text = (
        f"Remetente: {sender_name}\n\n"
        f"Mensagem de manutenção:\n{content}\n\n"
        "Atenciosamente,\nEquipe Cinema"
    )

    sucesso = _mailgun_send(subject, text)
    if not sucesso:
        return jsonify({"msg": "Falha ao enviar e-mail de manutenção."}), 500

    return jsonify({"msg": "E-mail de manutenção enviado com sucesso."}), 200