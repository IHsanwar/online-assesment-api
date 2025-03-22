from flask import Flask, request, jsonify
import os
from google.oauth2 import id_token
import google.auth.transport.requests
import jwt
import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "sqlite:///users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET'] = os.getenv("JWT_SECRET", "jwt-secret-key")
app.config['JWT_EXPIRATION'] = 3600  # 1 hour

# Database setup
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    google_id = db.Column(db.String(120), unique=True)
    picture = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'picture': self.picture
        }

# Google credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token, 
            google.auth.transport.requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        return id_info
    except ValueError:
        return None

def generate_jwt(user):
    """Generate a JWT token for the user"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=app.config['JWT_EXPIRATION']),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')

def jwt_required(f):
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            payload = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
            user = User.query.filter_by(id=payload['user_id']).first()
            if not user:
                return jsonify({'message': 'Invalid token: User not found!'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
            
        return f(user, *args, **kwargs)
    return decorated_function



# API endpoints
@app.route("/api/auth/google", methods=["POST"])
def google_auth():
    data = request.get_json()
    google_token = data.get("google_token")
    
    if not google_token:
        return jsonify({"error": "Google token is required"}), 400
    
    user_info = verify_google_token(google_token)
    
    if not user_info:
        return jsonify({"error": "Invalid Google token"}), 400
    
    # Find or create user
    user = User.query.filter_by(email=user_info['email']).first()
    
    if not user:
        user = User(
            email=user_info['email'],
            name=user_info.get('name', ''),
            google_id=user_info.get('sub'),
            picture=user_info.get('picture', '')
        )
        db.session.add(user)
        db.session.commit()
    
    # Generate JWT token
    jwt_token = generate_jwt(user)
    
    return jsonify({
        "token": jwt_token,
        "expires_in": app.config['JWT_EXPIRATION'],
        "user": user.to_dict()
    })

@app.route("/api/me", methods=["GET"])
@jwt_required
def get_me(current_user):
    return jsonify(current_user.to_dict())

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)