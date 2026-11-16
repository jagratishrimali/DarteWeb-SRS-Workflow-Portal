from datetime import datetime

from extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    srs_content = db.Column(db.Text, nullable=False)
    review_status = db.Column(db.String(20), default='draft', nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    steps = db.relationship('WorkflowStep', backref='project', cascade='all, delete-orphan', lazy=True)
    comments = db.relationship('Comment', backref='project', cascade='all, delete-orphan', lazy=True)
    memory_entries = db.relationship('MemoryEntry', backref='project', cascade='all, delete-orphan', lazy=True)
