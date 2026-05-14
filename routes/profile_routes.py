from flask import Blueprint, request, jsonify
from utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/admin-profile", methods=["GET"])
def get_profile():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin_profile LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return jsonify({
            "id": row["id"],
            "full_name": row["full_name"],
            "email": row["email"],
            "whatsapp": row["whatsapp"],
            "github": row["github"]
        })

    return jsonify({})


@profile_bp.route("/admin-profile", methods=["POST"])
def save_profile():
    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    whatsapp = data.get("whatsapp")
    github = data.get("github")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM admin_profile LIMIT 1")
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE admin_profile
            SET full_name=?, email=?, whatsapp=?, github=?
            WHERE id=?
        """, (
            full_name,
            email,
            whatsapp,
            github,
            existing["id"]
        ))
    else:
        cursor.execute("""
            INSERT INTO admin_profile (
                full_name,
                email,
                whatsapp,
                github
            )
            VALUES (?, ?, ?, ?)
        """, (
            full_name,
            email,
            whatsapp,
            github
        ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Profile updated successfully"
    })


@profile_bp.route("/change-password", methods=["POST"])
def change_password():
    data = request.json

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    conn = get_db()
    cursor = conn.cursor()

    admin = cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        ("admin",)
    ).fetchone()

    if not admin:
        conn.close()
        return jsonify({
            "message": "Admin not found"
        }), 404

    if not check_password_hash(admin["password"], old_password):
        conn.close()
        return jsonify({
            "message": "Old password is incorrect"
        }), 400

    hashed_password = generate_password_hash(new_password)

    cursor.execute("""
        UPDATE admins
        SET password=?
        WHERE username=?
    """, (
        hashed_password,
        "admin"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Password changed successfully"
    })