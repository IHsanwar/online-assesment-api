from flask import Blueprint, redirect, request, session, url_for, jsonify
import requests
from config import Config
from Models.Connection import db
from Models.User import User

auth_bp = Blueprint("auth", __name__)

def get_google_provider_cfg():
    return requests.get(Config.GOOGLE_DISCOVERY_URL).json()

@auth_bp.route("/login")
def login():
    google_cfg = get_google_provider_cfg()
    auth_endpoint = google_cfg["authorization_endpoint"]

    request_uri = (
        f"{auth_endpoint}?response_type=code"
        f"&client_id={Config.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={url_for('auth.callback', _external=True)}"
        f"&scope=openid email profile"
    )
    return redirect(request_uri)

@auth_bp.route("/callback")
def callback():
    google_cfg = get_google_provider_cfg()
    token_endpoint = google_cfg["token_endpoint"]

    code = request.args.get("code")
    token_data = {
        "code": code,
        "client_id": Config.GOOGLE_CLIENT_ID,
        "client_secret": Config.GOOGLE_CLIENT_SECRET,
        "redirect_uri": url_for("auth.callback", _external=True),
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_endpoint, data=token_data)
    token_json = token_response.json()
    userinfo_endpoint = google_cfg["userinfo_endpoint"]

    headers = {"Authorization": f"Bearer {token_json['access_token']}"}
    userinfo_response = requests.get(userinfo_endpoint, headers=headers).json()

    user = User.query.filter_by(google_id=userinfo_response["sub"]).first()
    if not user:
        user = User(
            google_id=userinfo_response["sub"],
            email=userinfo_response["email"],
            name=userinfo_response["name"],
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    return jsonify({"message": "Login successful", "user": userinfo_response})

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})
