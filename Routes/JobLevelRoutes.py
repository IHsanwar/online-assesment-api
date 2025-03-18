from flask import Blueprint, request
from Controllers.JobLevelController import JobLevelController

job_level_bp = Blueprint("job_level", __name__)

@job_level_bp.route("/job_levels", methods=["GET"])
def get_all_job_levels():
    return JobLevelController.get_all_job_levels()

@job_level_bp.route("/job_levels/<int:job_level_id>", methods=["GET"])
def get_job_level(job_level_id):
    return JobLevelController.get_job_level(job_level_id)

@job_level_bp.route("/job_levels", methods=["POST"])
def add_job_level():
    data = request.get_json()
    return JobLevelController.add_job_level(data)

@job_level_bp.route("/job_levels/<int:job_level_id>", methods=["PUT"])
def update_job_level(job_level_id):
    data = request.get_json()
    return JobLevelController.update_job_level(job_level_id, data)

@job_level_bp.route("/job_levels/<int:job_level_id>", methods=["DELETE"])
def delete_job_level(job_level_id):
    return JobLevelController.delete_job_level(job_level_id)
