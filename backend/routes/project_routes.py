from flask import Blueprint, session

from controllers.project_controller import create_project, delete_project, get_project, get_projects, publish_project, update_project
from models.user import User
from utils.decorators import login_required, role_required

project_bp = Blueprint('project_bp', __name__)


@project_bp.get('/projects')
@login_required
def list_projects():
    user = User.query.get(session['user_id'])
    return get_projects(user)


@project_bp.post('/projects')
@login_required
@role_required('admin')
def create_project_route():
    user = User.query.get(session['user_id'])
    return create_project(user)


@project_bp.get('/projects/<int:project_id>')
@login_required
def get_project_route(project_id):
    user = User.query.get(session['user_id'])
    return get_project(user, project_id)


@project_bp.put('/projects/<int:project_id>')
@login_required
@role_required('admin')
def update_project_route(project_id):
    user = User.query.get(session['user_id'])
    return update_project(user, project_id)


@project_bp.delete('/projects/<int:project_id>')
@login_required
@role_required('admin')
def delete_project_route(project_id):
    user = User.query.get(session['user_id'])
    return delete_project(user, project_id)


@project_bp.post('/projects/<int:project_id>/publish')
@login_required
@role_required('admin')
def publish_project_route(project_id):
    user = User.query.get(session['user_id'])
    return publish_project(user, project_id)
