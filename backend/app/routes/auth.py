from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token
from app.util.util import verify_password, hash_password
import psycopg2
import string
import secrets
import smtplib
from server import get_db

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

    access_token = create_access_token(identity={"username": user['username'], "role": user['role']})
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

def generate_password(tamanho=12):
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alfabeto) for _ in range(tamanho))

def send_recover_password_email(destinatario, senha_nova):
    remetente = "cinemapp_notification@gmail.com"
    senha_remetente = "senha123"

    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remetente, senha_remetente)

    assunto = "Recuperação de Senha"
    corpo = f"Sua nova senha é: {senha_nova}"

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    servidor.sendmail(remetente, destinatario, msg.as_string())
    servidor.quit()

@auth_bp.route("/recoverpassword", methods=["POST"])
def recover_password():
    data = request.json
    email = data.get("email")

    cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"msg": "E-mail não encontrado!"}), 404
    
    nova_senha = generate_password()

    hashed_password = hash_password(nova_senha)
    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
    cursor.connection.commit()

    send_recover_password_email(email, nova_senha)

    return jsonify({"msg": "Senha recuperada com sucesso! Verifique seu e-mail."}), 200
