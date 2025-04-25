from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import create_access_token
from app.util.util import verify_password
import psycopg2
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

