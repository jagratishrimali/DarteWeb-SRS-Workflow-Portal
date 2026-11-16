from flask import jsonify

from models.memory import MemoryEntry
from models.project import Project


def serialize_memory(memory):
    approver = memory.approved_by
    return {
        'id': memory.id,
        'project_id': memory.project_id,
        'step_id': memory.step_id,
        'source_comment_id': memory.source_comment_id,
        'approved_text': memory.approved_text,
        'approved_by': approver,
        'approved_at': memory.approved_at.isoformat() if memory.approved_at else None,
        'step_title': memory.workflow_step.title if memory.workflow_step else None,
        'source_comment': memory.source_comment.body if memory.source_comment else None,
    }


def get_memory(project_id):
    project = Project.query.get_or_404(project_id)
    entries = MemoryEntry.query.filter_by(project_id=project_id).order_by(MemoryEntry.approved_at.desc()).all()
    return jsonify({'project_id': project_id, 'memory_entries': [serialize_memory(entry) for entry in entries]}), 200


def export_memory(project_id):
    entries = MemoryEntry.query.filter_by(project_id=project_id).order_by(MemoryEntry.approved_at.asc()).all()
    lines = [f'# Memory File - Project {project_id}', '']
    for idx, entry in enumerate(entries, start=1):
        lines.append(f'## Entry {idx}')
        lines.append(f'- Workflow Step: {entry.workflow_step.title if entry.workflow_step else "Unknown"}')
        lines.append(f'- Approved By: Admin ID {entry.approved_by}')
        lines.append(f'- Approved At: {entry.approved_at.isoformat() if entry.approved_at else "Unknown"}')
        lines.append(f'- Original Comment: {entry.source_comment.body if entry.source_comment else "N/A"}')
        lines.append(f'- Approved Feedback: {entry.approved_text}')
        lines.append('')
    return '\n'.join(lines), 200, {'Content-Type': 'text/markdown; charset=utf-8', 'Content-Disposition': f'attachment; filename="memory_project_{project_id}.md"'}
