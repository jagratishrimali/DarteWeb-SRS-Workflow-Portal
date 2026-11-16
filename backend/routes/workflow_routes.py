from flask import Blueprint, session

from controllers.workflow_controller import create_step, delete_step, get_steps, reorder_steps, update_step
from models.user import User
from utils.decorators import login_required, role_required

workflow_bp = Blueprint('workflow_bp', __name__)


@workflow_bp.get('/projects/<int:project_id>/steps')
@login_required
def list_steps(project_id):
    return get_steps(project_id)


@workflow_bp.post('/steps')
@login_required
@role_required('admin')
def create_step_route():
    return create_step()


@workflow_bp.put('/steps/<int:step_id>')
@login_required
@role_required('admin')
def update_step_route(step_id):
    return update_step(step_id)


@workflow_bp.delete('/steps/<int:step_id>')
@login_required
@role_required('admin')
def delete_step_route(step_id):
    return delete_step(step_id)


@workflow_bp.put('/projects/<int:project_id>/steps/reorder')
@login_required
@role_required('admin')
def reorder_steps_route(project_id):
    return reorder_steps(project_id)
