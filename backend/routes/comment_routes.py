from flask import Blueprint, session

from controllers.comment_controller import create_comment, get_my_comments, get_project_comments, review_comment
from models.user import User
from utils.decorators import login_required, role_required

comment_bp = Blueprint('comment_bp', __name__)


@comment_bp.post('/comments')
@login_required
def create_comment_route():
    user = User.query.get(session['user_id'])
    return create_comment(user)


@comment_bp.get('/projects/<int:project_id>/comments')
@login_required
def project_comments(project_id):
    user = User.query.get(session['user_id'])
    return get_project_comments(user, project_id)


@comment_bp.get('/comments/my')
@login_required
def my_comments():
    user = User.query.get(session['user_id'])
    return get_my_comments(user)


@comment_bp.put('/comments/<int:comment_id>/review')
@login_required
@role_required('admin')
def review_comment_route(comment_id):
    user = User.query.get(session['user_id'])
    return review_comment(user, comment_id)
