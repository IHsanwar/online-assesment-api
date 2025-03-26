from flask import Flask, request, jsonify, redirect,url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os, google
# Import semua blueprint
from Routes import (
    CompetencyKeyRoutes, SectorRoutes,ScoreRoutes,
    IndicatorRoutes, CompetencyCategoryRoutes, JobLevelRoutes, JobFunctionRoute,
    AssesmentRoleRoutes,MainRoutes,EvidenceRoutes
) 
 


app = Flask(__name__)
app.secret_key = 'secret_key_word'
appjwt = JWTManager(app)
 
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "secret_key_word")  # Set secret key

CORS(app)

# Middleware: Hanya untuk logging
@app.before_request
def log_request_info():
    """Logging untuk request, tidak digunakan untuk autentikasi"""
    print(f"Incoming request: {request.method} {request.path}")


# 📌 Mendaftarkan semua blueprint#
app.register_blueprint(MainRoutes.main_bp)
app.register_blueprint(EvidenceRoutes.evidence_bp, url_prefix='/evidences')
app.register_blueprint(CompetencyKeyRoutes.competency_key_bp)
app.register_blueprint(IndicatorRoutes.indicator_bp)
app.register_blueprint(CompetencyCategoryRoutes.competency_category_bp)
app.register_blueprint(JobFunctionRoute.job_function_bp)
app.register_blueprint(JobLevelRoutes.job_level_bp)
app.register_blueprint(AssesmentRoleRoutes.assessment_role_bp)
app.register_blueprint(SectorRoutes.sector_bp)
app.register_blueprint(ScoreRoutes.score_bp )

if __name__ == "__main__":
    app.run(debug=True)
