from datetime import datetime

from extensions import db


class MemoryEntry(db.Model):
    __tablename__ = 'memory_entries'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('workflow_steps.id'), nullable=False)
    source_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False, unique=True)
    approved_text = db.Column(db.Text, nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('source_comment_id', name='uq_memory_source_comment'),
    )
