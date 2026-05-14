import sqlite3
from werkzeug.security import generate_password_hash


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    return get_db_connection()


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        tech_stack TEXT,
        github_link TEXT,
        live_link TEXT,
        images TEXT,
        features TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Admins Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Contacts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT,
        message TEXT NOT NULL
    )
    """)

    # Skills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        level TEXT NOT NULL
    )
    """)

    # Services Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL
    )
    """)

    # About Table
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

    # Admin Profile Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        whatsapp TEXT,
        github TEXT
    )
    """)

    # Default Admin
    admin = cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        ("admin",)
    ).fetchone()

    if not admin:
        hashed_password = generate_password_hash("123456")

        cursor.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            ("admin", hashed_password)
        )

    # Default About Data
    about = cursor.execute("SELECT * FROM about").fetchone()

    if not about:
        cursor.execute("""
        INSERT INTO about (
            title, highlight_word, description,

            exp_years, exp_text,
            projects_done, projects_text,
            focus_percent, focus_text,

            card1_title, card1_desc,
            card2_title, card2_desc,
            card3_title, card3_desc
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Creating Digital Solutions With",
            "Purpose",
            "I'm Muhammad Rizwan, a dedicated Software Engineer with 4+ years of experience building Flutter mobile apps, modern websites, and clean UI/UX experiences.",

            "4+",
            "Years Experience",

            "20+",
            "Projects Completed",

            "100%",
            "Client Focused",

            "Flutter Apps",
            "Cross-platform Android & iOS apps with premium UI.",

            "Web Development",
            "Responsive business websites and web solutions.",

            "UI / UX Design",
            "Modern user interfaces designed in Figma."
        ))

    # Default Admin Profile
    profile = cursor.execute(
        "SELECT * FROM admin_profile"
    ).fetchone()

    if not profile:
        cursor.execute("""
        INSERT INTO admin_profile (
            full_name,
            email,
            whatsapp,
            github
        )
        VALUES (?, ?, ?, ?)
        """, (
            "Muhammad Rizwan",
            "",
            "",
            ""
        ))

    conn.commit()
    conn.close()