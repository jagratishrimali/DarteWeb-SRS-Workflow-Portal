from datetime import datetime

from flask import jsonify, request

from extensions import db
from models.project import Project
from models.workflow import WorkflowStep


def serialize_step(step):
    return {
        'id': step.id,
        'project_id': step.project_id,
        'title': step.title,
        'description': step.description,
        'sequence': step.sequence,
        'created_at': step.created_at.isoformat() if step.created_at else None,
        'updated_at': step.updated_at.isoformat() if step.updated_at else None,
    }


def get_steps(project_id):
    project = Project.query.get_or_404(project_id)
    steps = WorkflowStep.query.filter_by(project_id=project_id).order_by(WorkflowStep.sequence.asc()).all()
    return jsonify({'steps': [serialize_step(s) for s in steps]}), 200


def create_step():
    data = request.get_json(silent=True) or {}
    project_id = data.get('project_id')
    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip()
    sequence = data.get('sequence')

    if not project_id or not title or not description:
        return jsonify({'error': 'Project ID, title and description are required'}), 400

    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    if sequence is None:
        max_sequence = db.session.query(db.func.max(WorkflowStep.sequence)).filter_by(project_id=project_id).scalar() or 0
        sequence = max_sequence + 1

    step = WorkflowStep(project_id=project_id, title=title, description=description, sequence=sequence)
    db.session.add(step)
    db.session.commit()
    return jsonify({'message': 'Workflow step created successfully', 'step': serialize_step(step)}), 201


def update_step(step_id):
    step = WorkflowStep.query.get_or_404(step_id)
    data = request.get_json(silent=True) or {}

    if 'title' in data and data['title']:
        step.title = data['title'].strip()
    if 'description' in data:
        step.description = (data['description'] or '').strip()
    if 'sequence' in data and data['sequence'] is not None:
        step.sequence = int(data['sequence'])

    step.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Workflow step updated successfully', 'step': serialize_step(step)}), 200


def delete_step(step_id):
    step = WorkflowStep.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({'message': 'Workflow step deleted successfully'}), 200


def reorder_steps(project_id):
    data = request.get_json(silent=True) or {}
    new_ids = data.get('step_order') or []
    if not isinstance(new_ids, list) or not new_ids:
        return jsonify({'error': 'step_order is required'}), 400

    project = Project.query.get_or_404(project_id)
    current_steps = WorkflowStep.query.filter_by(project_id=project_id).all()
    current_map = {step.id: step for step in current_steps}

    for idx, step_id in enumerate(new_ids, start=1):
        if step_id not in current_map:
            return jsonify({'error': f'Step {step_id} is not part of this project'}), 400
        current_map[step_id].sequence = idx

    db.session.commit()
    steps = WorkflowStep.query.filter_by(project_id=project_id).order_by(WorkflowStep.sequence.asc()).all()
    return jsonify({'message': 'Workflow steps reordered successfully', 'steps': [serialize_step(step) for step in steps]}), 200
