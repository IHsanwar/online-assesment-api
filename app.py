import sqlite3
from flask import Flask, request, jsonify, session, redirect
from dotenv import load_dotenv
import os

from Routes import ScoreRoutes, EvidenceRoutes, CompetencyKeyRoutes, SectorRoutes, IndicatorRoutes, CompetencyCategoryRoutes, JobLevelRoutes, JobFunctionRoute, AssesmentRoleRoutes
from Models.Connection import SessionLocal, Base, engine
from Controllers.MiddlewareController import *
from Controllers.LoginController import *
app = Flask(__name__)
load_dotenv()

# Set up authentication routes
setup_auth_routes(app)

# Register all your blueprints normally (without secure_blueprint)
app.register_blueprint(ScoreRoutes.score_bp)
app.register_blueprint(EvidenceRoutes.evidence_bp)
app.register_blueprint(CompetencyKeyRoutes.competency_key_bp)
app.register_blueprint(IndicatorRoutes.indicator_bp)
app.register_blueprint(CompetencyCategoryRoutes.competency_category_bp)
app.register_blueprint(JobFunctionRoute.job_function_bp)
app.register_blueprint(JobLevelRoutes.job_level_bp)
app.register_blueprint(AssesmentRoleRoutes.assessment_role_bp)
app.register_blueprint(SectorRoutes.sector_bp)

# Set database URL
DATABASE_URL = os.getenv("DATABASE_URL")



# Global middleware
@app.before_request
def check_auth():
    public_routes = ['/login', '/callback', '/logout']
    
    if request.path not in public_routes:
        if "user_info" not in session:
            # If requesting API endpoint (expecting JSON)
            if request.path.startswith('/') and request.headers.get('Accept') == 'application/json':
                return jsonify({"error": "Authentication required", "login_url": "/login"}), 401
            # Otherwise redirect to login page
            return redirect("/login")

if __name__ == '__main__':
    app.run(use_reloader=False, debug=os.getenv("DEBUG_MODE") == 'True')