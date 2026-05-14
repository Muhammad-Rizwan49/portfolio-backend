from flask import Blueprint, request, jsonify
from utils.db import get_db
from routes.auth_routes import token_required

contact_bp = Blueprint("contact_bp", __name__)


# ---------------- PUBLIC ROUTE ---------------- #

@contact_bp.route("/contact", methods=["POST"])
def save_contact():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({
            "error": "All fields are required"
        }), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contacts (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Message sent successfully"
    })


# ---------------- PROTECTED ADMIN ROUTE ---------------- #

@contact_bp.route("/contact", methods=["GET"])
@token_required
def get_contacts():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, message
        FROM contacts
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    contacts = []

    for row in rows:
        contacts.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "message": row["message"]
        })

    return jsonify(contacts)


# ---------------- DELETE MESSAGE ---------------- #

@contact_bp.route("/contact/<int:id>", methods=["DELETE"])
@token_required
def delete_contact(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Message deleted successfully"
    })