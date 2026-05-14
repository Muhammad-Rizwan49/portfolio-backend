from flask import Blueprint, request, jsonify
from utils.db import get_db
from routes.auth_routes import token_required

about_bp = Blueprint("about_bp", __name__)


@about_bp.route("/about/init", methods=["GET"])
def init_about():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS about (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,
            highlight_word TEXT,
            description TEXT,

            exp_years TEXT,
            exp_text TEXT,

            projects_done TEXT,
            projects_text TEXT,

            focus_percent TEXT,
            focus_text TEXT,

            card1_title TEXT,
            card1_desc TEXT,

            card2_title TEXT,
            card2_desc TEXT,

            card3_title TEXT,
            card3_desc TEXT
        )
    """)

    conn.commit()
    conn.close()

    return jsonify({"message": "About table ready"})


# ---------------- PUBLIC ROUTE ---------------- #

@about_bp.route("/about", methods=["GET"])
def get_about():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM about LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return jsonify({
            "id": row[0],
            "title": row[1],
            "highlight_word": row[2],
            "description": row[3],

            "exp_years": row[4],
            "exp_text": row[5],

            "projects_done": row[6],
            "projects_text": row[7],

            "focus_percent": row[8],
            "focus_text": row[9],

            "card1_title": row[10],
            "card1_desc": row[11],

            "card2_title": row[12],
            "card2_desc": row[13],

            "card3_title": row[14],
            "card3_desc": row[15]
        })

    return jsonify({})


# ---------------- PROTECTED ADMIN ROUTE ---------------- #

@about_bp.route("/about", methods=["POST"])
@token_required
def save_about():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM about LIMIT 1")
    existing = cursor.fetchone()

    values = (
        data.get("title"),
        data.get("highlight_word"),
        data.get("description"),

        data.get("exp_years"),
        data.get("exp_text"),

        data.get("projects_done"),
        data.get("projects_text"),

        data.get("focus_percent"),
        data.get("focus_text"),

        data.get("card1_title"),
        data.get("card1_desc"),

        data.get("card2_title"),
        data.get("card2_desc"),

        data.get("card3_title"),
        data.get("card3_desc")
    )

    if existing:
        cursor.execute("""
            UPDATE about SET
            title=?,
            highlight_word=?,
            description=?,
            exp_years=?,
            exp_text=?,
            projects_done=?,
            projects_text=?,
            focus_percent=?,
            focus_text=?,
            card1_title=?,
            card1_desc=?,
            card2_title=?,
            card2_desc=?,
            card3_title=?,
            card3_desc=?
            WHERE id=?
        """, values + (existing[0],))
    else:
        cursor.execute("""
            INSERT INTO about (
                title,
                highlight_word,
                description,
                exp_years,
                exp_text,
                projects_done,
                projects_text,
                focus_percent,
                focus_text,
                card1_title,
                card1_desc,
                card2_title,
                card2_desc,
                card3_title,
                card3_desc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)

    conn.commit()
    conn.close()

    return jsonify({"message": "About saved successfully"})