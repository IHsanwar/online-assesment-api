from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from Models.Connection import SessionLocal
from Models.JobFunction import JobFunction
from Models.JobLevel import JobLevel

job_function_bp = Blueprint('job_function', __name__)

class JobFunctionController:
    
    @staticmethod
    def get_all_job_functions():
        session = SessionLocal()
        job_functions = session.query(JobFunction).all()
        session.close()

        return jsonify([
            {
                "id": jf.id,
                "code": jf.code,
                "label": jf.label,
                "level_id": jf.level_id,
                "definisi": jf.definisi
            }
            for jf in job_functions
        ])

    @staticmethod
    def get_job_function(job_function_id):
        session = SessionLocal()
        job_function = session.query(JobFunction).filter_by(id=job_function_id).first()
        session.close()

        if not job_function:
            return jsonify({"error": "Job Function not found"}), 404

        return jsonify({
            "id": job_function.id,
            "code": job_function.code,
            "label": job_function.label,
            "level_id": job_function.level_id,
            "definisi": job_function.definisi
        })

    @staticmethod
    def add_job_function():
        data = request.get_json()
        session = SessionLocal()

        # Validate level_id exists
        level = session.query(JobLevel).filter_by(id=data["level_id"]).first()
        if not level:
            session.close()
            return jsonify({"error": "Invalid level_id"}), 400

        new_job_function = JobFunction(
            code=data["code"],
            label=data["label"],
            level_id=data["level_id"],
            definisi=data.get("definisi")
        )

        session.add(new_job_function)
        session.commit()
        session.close()

        return jsonify({"message": "Job Function added successfully"}), 201

    @staticmethod
    def update_job_function(job_function_id):
        data = request.get_json()
        session = SessionLocal()

        job_function = session.query(JobFunction).filter_by(id=job_function_id).first()
        if not job_function:
            session.close()
            return jsonify({"error": "Job Function not found"}), 404

        # Validate level_id if updated
        if "level_id" in data:
            level = session.query(JobLevel).filter_by(id=data["level_id"]).first()
            if not level:
                session.close()
                return jsonify({"error": "Invalid level_id"}), 400

        job_function.code = data.get("code", job_function.code)
        job_function.label = data.get("label", job_function.label)
        job_function.level_id = data.get("level_id", job_function.level_id)
        job_function.definisi = data.get("definisi", job_function.definisi)

        session.commit()
        session.close()

        return jsonify({"message": "Job Function updated successfully"})

    @staticmethod
    def delete_job_function(job_function_id):
        session = SessionLocal()

        job_function = session.query(JobFunction).filter_by(id=job_function_id).first()
        if not job_function:
            session.close()
            return jsonify({"error": "Job Function not found"}), 404

        session.delete(job_function)
        session.commit()
        session.close()

        return jsonify({"message": "Job Function deleted successfully"})
