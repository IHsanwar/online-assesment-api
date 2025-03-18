from Controllers.JobFunctionController import JobFunctionController
from flask import Blueprint, jsonify, request

job_function_bp = Blueprint('job_function', __name__)

@job_function_bp.route('/job_functions', methods=['GET'])
def get_all_job_functions():
    return JobFunctionController.get_all_job_functions()

@job_function_bp.route('/job_functions/<int:job_function_id>', methods=['GET'])
def get_job_function(job_function_id):
    return JobFunctionController.get_job_function(job_function_id)

@job_function_bp.route('/job_functions', methods=['POST'])
def add_job_function():
    return JobFunctionController.add_job_function()

@job_function_bp.route('/job_functions/<int:job_function_id>', methods=['PUT'])
def update_job_function(job_function_id):
    return JobFunctionController.update_job_function(job_function_id)

@job_function_bp.route('/job_functions/<int:job_function_id>', methods=['DELETE'])
def delete_job_function(job_function_id):
    return JobFunctionController.delete_job_function(job_function_id)
