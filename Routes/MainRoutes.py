from flask import Blueprint, request, redirect, Flask,jsonify
import os
import requests, jwt, datetime
from authlib.integrations.flask_client import OAuth 
from flask_jwt_extended import get_jwt_identity,create_access_token,jwt_required
oauth = OAuth(Flask(__name__))
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID', 'None') , # Ganti dengan Client ID Anda
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', ''), # Ganti dengan Client Secret Anda
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},  # Scope untuk mendapatkan informasi pengguna
)

TOKEN_URL = 'https://oauth2.googleapis.com/token' 
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

main_bp = Blueprint("default", __name__)
# Google OAuth
@main_bp.route("/login-google")
def login_google():
    auth_url = (
        f"{google.authorize_url}?"
        f"response_type=code&"
        f"client_id={google.client_id}&"
        f"redirect_uri=http://localhost:5000/callback&"
        f"scope=openid%20email%20profile&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return redirect(auth_url)
                                     
@main_bp.route("/callback")
def callback_google():
    # Ambil authorization code dari query string
    auth_code = request.args.get('code')

    # Exchange authorization code untuk access token
    token_data = {
        'code': auth_code,
        'client_id': google.client_id,
        'client_secret': google.client_secret,
        'redirect_uri': 'http://localhost:5000/callback',
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(TOKEN_URL, data=token_data)
    token_info = token_response.json() 

    headers = {'Authorization': f"Bearer {token_info['access_token']}"}
    user_info_response = requests.get(USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

    jwt_user = {
        'email': user_info['email'],
        'name': user_info['name'],
    }
    return generate_jwt(jwt_user) 
     

def generate_jwt(user):
    """Generate a JWT token for the user"""
    payload = {
        'user_name': user['name'],
        'email': user['email'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600),
        'iat': datetime.datetime.utcnow()
    } 
    access_token = create_access_token(identity=user['email'], additional_claims={"name": user['name']}) # Add sub claim here

    return access_token  

# Login (menghasilkan token)
@main_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    user_email = data["email"]
    
    # Simulasi autentikasi (seharusnya cek database)
    if user_email != "test@example.com":
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user_email)
    
    return jsonify({"token": access_token})

# Route terlindungi contoh

@main_bp.route("/protected", methods=["GET"]) 
@jwt_required() 
def protected():
    """Endpoint hanya bisa diakses dengan token valid"""
    current_user = get_jwt_identity()
    return jsonify({"message": "Access granted", "user": current_user})
