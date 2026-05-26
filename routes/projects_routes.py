from flask import Blueprint, request, jsonify
import os
import uuid
import json

from werkzeug.utils import secure_filename

from utils.db import get_db_connection

project_bp = Blueprint("projects", __name__)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# Get projects
@project_bp.route(
    "/projects",
    methods=["GET"]
)
def get_projects():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM projects
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    projects = []

    for row in rows:

        projects.append({
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "tech_stack": row["tech_stack"],
            "github_link": row["github_link"],
            "live_link": row["live_link"],
            "images": json.loads(
                row["images"] or "[]"
            ),
            "created_at": row["created_at"]
        })

    conn.close()

    return jsonify(projects)


# Add project
@project_bp.route(
    "/projects",
    methods=["POST"]
)
def add_project():

    title = request.form.get("title")

    description = request.form.get(
        "description"
    )

    tech_stack = request.form.get(
        "tech_stack"
    )

    github_link = request.form.get(
        "github_link"
    )

    live_link = request.form.get(
        "live_link"
    )

    image_files = request.files.getlist(
        "images"
    )

    uploaded_images = []

    for image in image_files:

        filename = secure_filename(
            image.filename
        )

        unique_name = (
            f"{uuid.uuid4().hex}_{filename}"
        )

        image_path = os.path.join(
            UPLOAD_FOLDER,
            unique_name
        )

        image.save(image_path)

        uploaded_images.append(
            unique_name
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projects (
            title,
            description,
            tech_stack,
            github_link,
            live_link,
            images
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        tech_stack,
        github_link,
        live_link,
        json.dumps(uploaded_images)
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message":
        "Project added successfully"
    })


# Update project
@project_bp.route(
    "/projects/<int:id>",
    methods=["PUT"]
)
def update_project(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM projects WHERE id=?",
        (id,)
    )

    project = cursor.fetchone()

    if not project:

        conn.close()

        return jsonify({
            "message":
            "Project not found"
        }), 404

    title = request.form.get("title")

    description = request.form.get(
        "description"
    )

    tech_stack = request.form.get(
        "tech_stack"
    )

    github_link = request.form.get(
        "github_link"
    )

    live_link = request.form.get(
        "live_link"
    )

    old_images = json.loads(
        project["images"] or "[]"
    )

    image_files = request.files.getlist(
        "images"
    )

    uploaded_images = []

    # Remove old images
    for image_name in old_images:

        image_path = os.path.join(
            UPLOAD_FOLDER,
            image_name
        )

        if os.path.exists(image_path):

            os.remove(image_path)

    # Save new images
    for image in image_files:

        filename = secure_filename(
            image.filename
        )

        unique_name = (
            f"{uuid.uuid4().hex}_{filename}"
        )

        image_path = os.path.join(
            UPLOAD_FOLDER,
            unique_name
        )

        image.save(image_path)

        uploaded_images.append(
            unique_name
        )

    cursor.execute("""
        UPDATE projects
        SET
            title=?,
            description=?,
            tech_stack=?,
            github_link=?,
            live_link=?,
            images=?
        WHERE id=?
    """, (
        title,
        description,
        tech_stack,
        github_link,
        live_link,
        json.dumps(uploaded_images),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message":
        "Project updated successfully"
    })


# Delete project
@project_bp.route(
    "/projects/<int:id>",
    methods=["DELETE"]
)
def delete_project(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM projects WHERE id=?",
        (id,)
    )

    project = cursor.fetchone()

    if not project:

        conn.close()

        return jsonify({
            "message":
            "Project not found"
        }), 404

    images = json.loads(
        project["images"] or "[]"
    )

    # Remove uploaded images
    for image_name in images:

        image_path = os.path.join(
            UPLOAD_FOLDER,
            image_name
        )

        if os.path.exists(image_path):

            os.remove(image_path)

    cursor.execute(
        "DELETE FROM projects WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message":
        "Project deleted successfully"
    })