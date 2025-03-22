import os

from flask import Blueprint, request, jsonify, redirect, url_for, Flask
from flask_jwt_extended import create_access_token
from flask_dance.contrib.google import make_google_blueprint, google
from Models.Connection import SessionLocal
from Models.User import User
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET'] = os.getenv("JWT_SECRET", "jwt-secret-key")

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, app.config['JWT_SECRET'], algorithm='HS256')

def jwt_required(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        
        token = token.split(" ")[1]

        try:
            decoded = jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
            return f(decoded['user_id'], *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get("user_id")  # Simulasi autentikasi

    if not user_id:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_jwt(user_id)
    return jsonify({"token": token})

@app.route('/protected', methods=['GET'])
@jwt_required
def protected(current_user):
    return jsonify({"message": "Success", "user_id": current_user})

if __name__ == '__main__':
    app.run(debug=True)
