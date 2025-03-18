from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from Models.Connection import SessionLocal
from Models.JobLevel import JobLevel
from Models.Sector import Sector

class JobLevelController:
    
    @staticmethod
    def get_all_job_levels():
        session = SessionLocal()
        try:
            job_levels = session.query(JobLevel).all()
            result = [
                {
                    "id": jl.id,
                    "sector_id": jl.sector_id,
                    "code": jl.code,
                    "title": jl.title
                }
                for jl in job_levels
            ]
            return jsonify(result)
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def get_job_level(job_level_id):
        session = SessionLocal()
        try:
            job_level = session.query(JobLevel).filter_by(id=job_level_id).first()
            if not job_level:
                return jsonify({"error": "Job Level not found"}), 404

            return jsonify({
                "id": job_level.id,
                "sector_id": job_level.sector_id,
                "code": job_level.code,
                "title": job_level.title
            })
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def add_job_level(data):
        session = SessionLocal()
        try:
            # Validate sector ID exists
            sector = session.query(Sector).filter_by(id=data["sector_id"]).first()
            if not sector:
                return jsonify({"error": "Invalid sector_id"}), 400

            new_job_level = JobLevel(
                sector_id=data["sector_id"],
                code=data["code"],
                title=data["title"]
            )
            session.add(new_job_level)
            session.commit()

            return jsonify({"message": "Job Level added successfully", "id": new_job_level.id}), 201
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def update_job_level(job_level_id, data):
        session = SessionLocal()
        try:
            job_level = session.query(JobLevel).filter_by(id=job_level_id).first()
            if not job_level:
                return jsonify({"error": "Job Level not found"}), 404

            job_level.sector_id = data.get("sector_id", job_level.sector_id)
            job_level.code = data.get("code", job_level.code)
            job_level.title = data.get("title", job_level.title)

            session.commit()
            return jsonify({"message": "Job Level updated successfully"})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def delete_job_level(job_level_id):
        session = SessionLocal()
        try:
            job_level = session.query(JobLevel).filter_by(id=job_level_id).first()
            if not job_level:
                return jsonify({"error": "Job Level not found"}), 404

            session.delete(job_level)
            session.commit()
            return jsonify({"message": "Job Level deleted successfully"})
        except SQLAlchemyError as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
