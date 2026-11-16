from flask import Blueprint

from controllers.auth_controller import current_user, login_user, logout_user
from utils.decorators import login_required


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.post('/login')
def login():
    return login_user()


@auth_bp.post('/logout')
@login_required
def logout():
    return logout_user()


@auth_bp.get('/me')
@login_required
def me():
    return current_user()
