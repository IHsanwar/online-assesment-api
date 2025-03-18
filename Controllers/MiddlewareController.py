from functools import wraps
from flask import Flask, redirect, session, url_for, request, jsonify
import os
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
import pathlib
import json
from dotenv import load_dotenv
# Configuration
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE","client_secret.json")  # Download this from Google Cloud Console
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"]
REDIRECT_URI = "http://localhost:5000/callback"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  


load_dotenv()

# Create a Flow object
def create_flow():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return flow

def verify_google_token(token):
    try:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        id_info = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), client_id)
        return id_info  # Returns user info like email, name, etc.
    except ValueError:
        return None  # Invalid token
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user_info = verify_google_token(token)
            if user_info:
                session["user_info"] = user_info  # Optional: store in session
                return f(*args, **kwargs)
        
        if "user_info" not in session:
            return jsonify({"error": "Authentication required", "login_url": "/login"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

# Routes to add to your Flask app
def setup_auth_routes(app):
    app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
    
    @app.route("/login")
    def login():
        flow = create_flow()
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        session["state"] = state
        return redirect(authorization_url)
    
    @app.route("/callback")
    def callback():
        flow = create_flow()
        
        # Ensure state matches to prevent CSRF attacks
        if session.get("state") != request.args.get("state"):
            return jsonify({"error": "State mismatch"}), 400
        
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
        
        id_info = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=token_request
        )
        
        # Store user info in session
        session["user_info"] = id_info
        
        # Redirect to original URL if available
        next_url = session.pop("next_url", "/")
        return redirect(next_url)
    
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")
    
    @app.route("/user")
    @login_required
    def get_user():
        return jsonify(session.get("user_info", {}))
    
def secure_blueprint(blueprint):
    """
    Secures all routes in a blueprint with the login_required decorator
    """
    for endpoint, view_func in blueprint.view_functions.items():
        blueprint.view_functions[endpoint] = login_required(view_func)
    return blueprint


"""
from middleware import setup_auth_routes, secure_blueprint, login_required

app = Flask(__name__)

# Set up auth routes
setup_auth_routes(app)

# Secure existing blueprints
app.register_blueprint(secure_blueprint(job_function_bp))

# Or secure individual routes
@app.route('/protected')
@login_required
def protected():
    return "This is a protected route"
"""