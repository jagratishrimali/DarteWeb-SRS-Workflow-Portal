from datetime import datetime

from flask import jsonify, request

from extensions import db
from models.comment import Comment
from models.project import Project
from models.workflow import WorkflowStep


def serialize_comment(comment):
    return {
        'id': comment.id,
        'step_id': comment.step_id,
        'project_id': comment.project_id,
        'client_id': comment.client_id,
        'body': comment.body,
        'status': comment.status,
        'admin_response': comment.admin_response or '',
        'created_at': comment.created_at.isoformat() if comment.created_at else None,
        'reviewed_at': comment.reviewed_at.isoformat() if comment.reviewed_at else None,
        'reviewed_by': comment.reviewed_by,
        'client': comment.client.to_dict() if comment.client else None,
        'workflow_step': {
            'id': comment.workflow_step.id,
            'title': comment.workflow_step.title,
            'sequence': comment.workflow_step.sequence,
        } if comment.workflow_step else None,
    }


def create_comment(user):
    data = request.get_json(silent=True) or {}
    step_id = data.get('step_id')
    body = (data.get('body') or '').strip()

    if not step_id or not body:
        return jsonify({'error': 'Step and comment body are required'}), 400

    step = WorkflowStep.query.get(step_id)
    if not step:
        return jsonify({'error': 'Workflow step not found'}), 404

    project = Project.query.get(step.project_id)
    if project.review_status != 'published':
        return jsonify({'error': 'Project is not published yet'}), 400

    if user.role != 'client':
        return jsonify({'error': 'Only client users can submit comments'}), 403

    comment = Comment(
        step_id=step.id,
        project_id=project.id,
        client_id=user.id,
        body=body,
        status='pending',
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment submitted successfully', 'comment': serialize_comment(comment)}), 201


def get_project_comments(user, project_id):
    project = Project.query.get_or_404(project_id)
    if user.role == 'admin':
        comments = Comment.query.filter_by(project_id=project_id).order_by(Comment.created_at.desc()).all()
    else:
        comments = Comment.query.filter_by(project_id=project_id, client_id=user.id).order_by(Comment.created_at.desc()).all()
    return jsonify({'comments': [serialize_comment(c) for c in comments]}), 200


def get_my_comments(user):
    comments = Comment.query.filter_by(client_id=user.id).order_by(Comment.created_at.desc()).all()
    return jsonify({'comments': [serialize_comment(c) for c in comments]}), 200


def review_comment(user, comment_id):
    if user.role != 'admin':
        return jsonify({'error': 'Only admin can review comments'}), 403

    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json(silent=True) or {}
    status = (data.get('status') or '').lower()
    admin_response = (data.get('admin_response') or '').strip()

    if status not in {'accepted', 'rejected'}:
        return jsonify({'error': 'Status must be accepted or rejected'}), 400

    if comment.status in {'accepted', 'rejected'}:
        return jsonify({'error': 'Comment has already been reviewed'}), 400

    comment.status = status
    comment.admin_response = admin_response
    comment.reviewed_by = user.id
    comment.reviewed_at = datetime.utcnow()

    if status == 'accepted':
        from models.memory import MemoryEntry
        if MemoryEntry.query.filter_by(source_comment_id=comment.id).first():
            db.session.commit()
            return jsonify({'message': 'Comment already approved', 'comment': serialize_comment(comment)}), 200

        memory_entry = MemoryEntry(
            project_id=comment.project_id,
            step_id=comment.step_id,
            source_comment_id=comment.id,
            approved_text=comment.body,
            approved_by=user.id,
        )
        db.session.add(memory_entry)

    db.session.commit()
    return jsonify({'message': f'Comment marked as {status}', 'comment': serialize_comment(comment)}), 200
