from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from werkzeug.utils import secure_filename
from routes.auth_routes import token_required
import os
import uuid

project_bp = Blueprint("project_bp", __name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- PUBLIC ROUTES ---------------- #

@project_bp.route("/projects", methods=["GET"])
def get_projects():
    conn = get_db_connection()

    projects = conn.execute("""
        SELECT * FROM projects
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in projects])


@project_bp.route("/projects/<int:id>", methods=["GET"])
def single_project(id):
    conn = get_db_connection()

    project = conn.execute(
        "SELECT * FROM projects WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if not project:
        return jsonify({
            "message": "Project not found"
        }), 404

    return jsonify(dict(project))


# ---------------- PROTECTED ADMIN ROUTES ---------------- #

@project_bp.route("/projects", methods=["POST"])
@token_required
def add_project():
    title = request.form.get("title")
    description = request.form.get("description")
    tech_stack = request.form.get("tech_stack")
    github_link = request.form.get("github_link")
    live_link = request.form.get("live_link")
    features = request.form.get("features")

    files = request.files.getlist("images")

    image_names = []

    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            unique_name = f"{uuid.uuid4().hex}_{filename}"

            file.save(
                os.path.join(UPLOAD_FOLDER, unique_name)
            )

            image_names.append(unique_name)

    images = ",".join(image_names)

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO projects
        (title, description, tech_stack, github_link, live_link, images, features)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        tech_stack,
        github_link,
        live_link,
        images,
        features
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Project added successfully"
    })


@project_bp.route("/projects/<int:id>", methods=["DELETE"])
@token_required
def delete_project(id):
    conn = get_db_connection()

    project = conn.execute(
        "SELECT images FROM projects WHERE id=?",
        (id,)
    ).fetchone()

    if project and project["images"]:
        files = project["images"].split(",")

        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file)

            if os.path.exists(path):
                os.remove(path)

    conn.execute(
        "DELETE FROM projects WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Project deleted successfully"
    })