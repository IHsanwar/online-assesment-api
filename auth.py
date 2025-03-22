import os
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token
from flask_dance.contrib.google import make_google_blueprint, google
from Models.Connection import SessionLocal
from Models.User import User
from datetime import timedelta

auth_bp = Blueprint("auth_bp", __name__)

# Google OAuth Blueprint
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="auth_bp.google_login"
)

auth_bp.register_blueprint(google_bp, url_prefix="/login")  # Pastikan ini ada

@auth_bp.route("/login/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))  # Pastikan ini sesuai
    
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        email = user_info.get("email")
        name = user_info.get("name")

        db = SessionLocal()
        try:
            user = db.query(User).filter_by(email=email).first()
            if not user:
                user = User(email=email, name=name)
                db.add(user)
                db.commit()

            access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
            return jsonify(access_token=access_token, user={"email": email, "name": name})
        finally:
            db.close()

    return jsonify({"error": "Google authentication failed"}), 400
