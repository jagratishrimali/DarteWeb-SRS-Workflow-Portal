from flask import Blueprint, session

from controllers.memory_controller import export_memory, get_memory
from models.user import User
from utils.decorators import login_required

memory_bp = Blueprint('memory_bp', __name__)


@memory_bp.get('/memory/<int:project_id>')
@login_required
def memory_entries(project_id):
    return get_memory(project_id)


@memory_bp.get('/memory/<int:project_id>/export')
@login_required
def export_memory_route(project_id):
    return export_memory(project_id)
