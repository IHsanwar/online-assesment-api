from flask import request, jsonify, session, Blueprint
from flask_jwt_extended import get_jwt_identity, JWTManager, verify_jwt_in_request, get_jwt
 
import jwt



# Create a blueprint for authentication-related routes (optional but good practice)
auth_bp = Blueprint('auth', __name__)


def check_bearer_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"msg": "Missing Authorization Header"}), 401

    if not auth_header.startswith('Bearer '):
        return jsonify({"msg": "Invalid Authorization Header Format"}), 401

    token = auth_header.split(' ')[1]

    try:
        # Verifikasi token JWT
        verify_jwt_in_request()
        claims = get_jwt()
        current_user = claims.get("sub")
        request.user = current_user  # Simpan identitas pengguna di request
        
    except Exception as e:
        return jsonify({"msg": "Invalid or Expired Token"}), 401

    return current_user


def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return wrapper
 
# Example usage within the blueprint (optional)
# @auth_bp.route('/protected', methods=['GET'])
# @bearer_token_required
# def protected_route():
#     return jsonify({"message": "This is a protected route", "user": request.user}), 200
