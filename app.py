import sqlite3
from flask import Flask, request, jsonify, session, redirect
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Depends, HTTPException, Header
import jwt
from Routes import ScoreRoutes, EvidenceRoutes, CompetencyKeyRoutes, SectorRoutes, IndicatorRoutes, CompetencyCategoryRoutes, JobLevelRoutes, JobFunctionRoute, AssesmentRoleRoutes
from Models.Connection import SessionLocal, Base, engine
from Controllers.LoginController import *
from auth import auth_bp,google_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "supersecretkey"

jwt = JWTManager(app)
CORS(app)

with app.app_context():
    Base.metadata.create_all(engine)

app.register_blueprint(ScoreRoutes.score_bp)
app.register_blueprint(EvidenceRoutes.evidence_bp)
app.register_blueprint(CompetencyKeyRoutes.competency_key_bp)
app.register_blueprint(IndicatorRoutes.indicator_bp)
app.register_blueprint(CompetencyCategoryRoutes.competency_category_bp)
app.register_blueprint(JobFunctionRoute.job_function_bp)
app.register_blueprint(JobLevelRoutes.job_level_bp)
app.register_blueprint(AssesmentRoleRoutes.assessment_role_bp)
app.register_blueprint(SectorRoutes.sector_bp)

GLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

@app.route("/login/google", methods=["GET"])
def google_login():
    """Redirect ke URL OAuth Google"""
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        "&redirect_uri=http://127.0.0.1:5000/callback"
        "&scope=openid%20email%20profile"
    )

    return redirect(google_auth_url)

@app.route("/callback", methods=["GET"])
def google_callback():
    """Menangani callback dari Google setelah login"""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Authorization code is missing"}), 400
    
    return jsonify({"message": "Google login successful", "code": code})

if __name__ == "__main__":
    app.run(debug=True)

@app.before_request
def check_auth():
    """Middleware untuk memeriksa autentikasi di setiap request API"""
    public_routes = ['/login', '/callback', '/logout', '/api/auth/google']

    # Bypass untuk route publik
    if request.path in public_routes:
        return

    token = None
    auth_header = request.headers.get('Authorization')

    if "user_info" in session:
        return  

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        if request.path.startswith('/api'):
            return jsonify({"error": "Authentication required", "login_url": "/api/auth/google"}), 401
        return redirect("/login/google")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        request.user = payload  # Simpan user ke request agar bisa diakses di route
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
if __name__ == '__main__':
    app.run(use_reloader=False, debug=os.getenv("DEBUG_MODE") == 'True')