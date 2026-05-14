from flask import Blueprint, request, jsonify
from functools import wraps
from utils.db import get_db_connection
from werkzeug.security import check_password_hash
import jwt
import datetime

auth_bp = Blueprint("auth_bp", __name__)

SECRET_KEY = "portfolio_secret_key_123"


# ---------------- LOGIN ---------------- #
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    conn = get_db_connection()

    admin = conn.execute(
        "SELECT * FROM admins WHERE username=?",
        (username,)
    ).fetchone()

    conn.close()

    if admin and check_password_hash(admin["password"], password):
        token = jwt.encode(
            {
                "username": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "message": "Login successful",
            "token": token
        })

    return jsonify({"message": "Invalid credentials"}), 401


# ---------------- TOKEN VERIFY DECORATOR ---------------- #
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]

            jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

        except Exception:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated