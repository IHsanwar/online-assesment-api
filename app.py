from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os

# Import semua blueprint
from Routes import (
    ScoreRoutes, EvidenceRoutes, CompetencyKeyRoutes, SectorRoutes,
    IndicatorRoutes, CompetencyCategoryRoutes, JobLevelRoutes, JobFunctionRoute,
    AssesmentRoleRoutes
)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")  # Set secret key
jwt = JWTManager(app)
CORS(app)

# Middleware: Hanya untuk logging
@app.before_request
def log_request_info():
    """Logging untuk request, tidak digunakan untuk autentikasi"""
    print(f"Incoming request: {request.method} {request.path}")

# Login (menghasilkan token)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    user_email = data["email"]
    
    # Simulasi autentikasi (seharusnya cek database)
    if user_email != "test@example.com":
        return jsonify({"error": "Invalid credentials"}), 401

    from flask_jwt_extended import create_access_token
    access_token = create_access_token(identity=user_email)
    
    return jsonify({"token": access_token})

# Route terlindungi contoh
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """Endpoint hanya bisa diakses dengan token valid"""
    current_user = get_jwt_identity()
    return jsonify({"message": "Access granted", "user": current_user})

# 📌 Mendaftarkan semua blueprint
app.register_blueprint(ScoreRoutes.score_bp)
app.register_blueprint(EvidenceRoutes.evidence_bp)
app.register_blueprint(CompetencyKeyRoutes.competency_key_bp)
app.register_blueprint(IndicatorRoutes.indicator_bp)
app.register_blueprint(CompetencyCategoryRoutes.competency_category_bp)
app.register_blueprint(JobFunctionRoute.job_function_bp)
app.register_blueprint(JobLevelRoutes.job_level_bp)
app.register_blueprint(AssesmentRoleRoutes.assessment_role_bp)
app.register_blueprint(SectorRoutes.sector_bp)

if __name__ == "__main__":
    app.run(debug=True)
