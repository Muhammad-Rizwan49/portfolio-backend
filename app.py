from flask import Flask
from flask_cors import CORS
from flask import send_from_directory
from routes.about_routes import about_bp
from utils.db import init_db
from routes.projects_routes import project_bp
from routes.auth_routes import auth_bp
from routes.contact_routes import contact_bp
from routes.skills_routes import skills_bp
from routes.services_routes import services_bp
from routes.profile_routes import profile_bp
from routes.admin_profile_routes import admin_profile_bp


app = Flask(__name__)
CORS(app)

init_db()

app.register_blueprint(project_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(services_bp)
app.register_blueprint(about_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_profile_bp)


@app.route("/")
def home():
    return {"message": "Portfolio Backend Running"}


@app.route("/uploads/<path:filename>")
def uploaded_files(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000)