from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.auth import token_required

services_bp = Blueprint("services", __name__)


@services_bp.route("/services", methods=["GET"])
def get_services():
    conn = get_db_connection()

    services = conn.execute(
        "SELECT * FROM services ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in services])


@services_bp.route("/services", methods=["POST"])
@token_required
def add_service():
    data = request.get_json()

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO services (title, description) VALUES (?, ?)",
        (data["title"], data["description"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Service added successfully"})


@services_bp.route("/services/<int:id>", methods=["DELETE"])
@token_required
def delete_service(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM services WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Service deleted successfully"})