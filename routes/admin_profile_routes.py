from flask import Blueprint, request, jsonify
from utils.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

admin_profile_bp = Blueprint("admin_profile_bp", __name__)


@admin_profile_bp.route("/admin-profile", methods=["GET"])
def get_profile():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin_profile LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if not row:
        return jsonify({})

    return jsonify({
        "full_name": row["full_name"],
        "email": row["email"],
        "whatsapp": row["whatsapp"],
        "github": row["github"]
    })


@admin_profile_bp.route("/admin-profile", methods=["POST"])
def save_profile():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE admin_profile
        SET full_name=?,
            email=?,
            whatsapp=?,
            github=?
        WHERE id=1
    """, (
        data.get("full_name"),
        data.get("email"),
        data.get("whatsapp"),
        data.get("github")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Profile updated"})


@admin_profile_bp.route("/change-password", methods=["POST"])
def change_password():
    data = request.json

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        ("admin",)
    )

    admin = cursor.fetchone()

    if not admin:
        conn.close()
        return jsonify({"message": "Admin not found"}), 404

    if not check_password_hash(admin["password"], old_password):
        conn.close()
        return jsonify({"message": "Wrong current password"}), 400

    new_hash = generate_password_hash(new_password)

    cursor.execute(
        "UPDATE admins SET password=? WHERE username=?",
        (new_hash, "admin")
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Password changed successfully"})