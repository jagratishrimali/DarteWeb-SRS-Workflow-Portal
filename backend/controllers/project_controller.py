from datetime import datetime

from flask import jsonify, request

from extensions import db
from models.project import Project
from models.user import User


def serialize_project(project):
    return {
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'srs_content': project.srs_content,
        'review_status': project.review_status,
        'client_id': project.client_id,
        'created_at': project.created_at.isoformat() if project.created_at else None,
        'updated_at': project.updated_at.isoformat() if project.updated_at else None,
        'client': project.client.to_dict() if project.client else None,
        'workflow_count': len(project.steps),
    }


def get_projects(user):
    if user.role == 'admin':
        projects = Project.query.order_by(Project.created_at.desc()).all()
    else:
        projects = Project.query.filter((Project.client_id == user.id) | (Project.review_status == 'published')).order_by(Project.created_at.desc()).all()
    return jsonify({'projects': [serialize_project(p) for p in projects]}), 200


def create_project(user):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    description = (data.get('description') or '').strip()
    srs_content = (data.get('srs_content') or '').strip()
    client_id = data.get('client_id')

    if not name or not description or not srs_content:
        return jsonify({'error': 'Name, description and SRS content are required'}), 400

    if user.role != 'admin':
        return jsonify({'error': 'Only admin can create projects'}), 403

    target_client = User.query.get(client_id) if client_id else User.query.filter_by(username='client').first()
    if not target_client:
        return jsonify({'error': 'Client user not found'}), 400

    project = Project(
        name=name,
        description=description,
        srs_content=srs_content,
        review_status='draft',
        client_id=target_client.id,
    )
    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully', 'project': serialize_project(project)}), 201


def get_project(user, project_id):
    project = Project.query.get_or_404(project_id)
    if user.role != 'admin' and project.client_id != user.id and project.review_status != 'published':
        return jsonify({'error': 'Project not available'}), 403
    return jsonify({'project': serialize_project(project)}), 200


def update_project(user, project_id):
    project = Project.query.get_or_404(project_id)
    if user.role != 'admin':
        return jsonify({'error': 'Only admin can update projects'}), 403

    data = request.get_json(silent=True) or {}
    if 'name' in data and data['name']:
        project.name = data['name'].strip()
    if 'description' in data:
        project.description = (data['description'] or '').strip()
    if 'srs_content' in data:
        project.srs_content = (data['srs_content'] or '').strip()
    if 'client_id' in data and data['client_id']:
        client = User.query.get(data['client_id'])
        if not client:
            return jsonify({'error': 'Client user not found'}), 400
        project.client_id = client.id

    project.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Project updated successfully', 'project': serialize_project(project)}), 200


def delete_project(user, project_id):
    project = Project.query.get_or_404(project_id)
    if user.role != 'admin':
        return jsonify({'error': 'Only admin can delete projects'}), 403

    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200


def publish_project(user, project_id):
    project = Project.query.get_or_404(project_id)
    if user.role != 'admin':
        return jsonify({'error': 'Only admin can publish a project'}), 403

    project.review_status = 'published'
    project.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Project published successfully', 'project': serialize_project(project)}), 200
