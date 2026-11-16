from datetime import datetime

from extensions import db


class WorkflowStep(db.Model):
    __tablename__ = 'workflow_steps'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='workflow_step', cascade='all, delete-orphan', lazy=True)
    memory_entries = db.relationship('MemoryEntry', backref='workflow_step', cascade='all, delete-orphan', lazy=True)
