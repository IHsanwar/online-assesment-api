import os

from flask import Blueprint, request, jsonify, redirect, url_for, Flask
from flask_jwt_extended import create_access_token
from flask_dance.contrib.google import make_google_blueprint, google
from Models.Connection import SessionLocal
from Models.User import User
from datetime import timedelta
  
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
