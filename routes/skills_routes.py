from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.auth import token_required

skills_bp = Blueprint("skills", __name__)


@skills_bp.route("/skills", methods=["GET"])
def get_skills():
    conn = get_db_connection()

    skills = conn.execute(
        "SELECT * FROM skills ORDER BY id ASC"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in skills])


@skills_bp.route("/skills", methods=["POST"])
@token_required
def add_skill():
    data = request.get_json()

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO skills (name, level) VALUES (?, ?)",
        (data["name"], data["level"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Skill added successfully"})


@skills_bp.route("/skills/<int:id>", methods=["DELETE"])
@token_required
def delete_skill(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM skills WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Skill deleted successfully"})