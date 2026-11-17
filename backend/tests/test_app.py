import os

import pytest
from werkzeug.security import generate_password_hash

# Unit tests use an isolated in-memory database, regardless of local .env settings.
os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from app import app, db
from models.comment import Comment
from models.memory import MemoryEntry
from models.project import Project
from models.user import User
from models.workflow import WorkflowStep


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(username='admin', password_hash=generate_password_hash('Admin@123'), role='admin')
        client_user = User(username='client', password_hash=generate_password_hash('Client@123'), role='client')
        db.session.add_all([admin, client_user])
        db.session.commit()

        project = Project(
            name='Test Project',
            description='Sample description',
            srs_content='System requirements',
            review_status='published',
            client_id=client_user.id,
        )
        db.session.add(project)
        db.session.commit()

        step = WorkflowStep(project_id=project.id, title='Discovery', description='Collect requirements', sequence=1)
        db.session.add(step)
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client


def test_login_as_admin_and_client(client):
    admin_login = client.post('/api/login', json={'username': 'admin', 'password': 'Admin@123'})
    assert admin_login.status_code == 200
    assert admin_login.get_json()['user']['role'] == 'admin'

    client.post('/api/logout')

    client_login = client.post('/api/login', json={'username': 'client', 'password': 'Client@123'})
    assert client_login.status_code == 200
    assert client_login.get_json()['user']['role'] == 'client'


def test_only_admin_can_delete_projects(client):
    with app.app_context():
        project_id = db.session.scalar(db.select(Project.id))

    client.post('/api/login', json={'username': 'client', 'password': 'Client@123'})
    forbidden = client.delete(f'/api/projects/{project_id}')
    assert forbidden.status_code == 403
    assert forbidden.get_json()['error'] == 'Admin role required'
    with app.app_context():
        assert db.session.get(Project, project_id) is not None

    client.post('/api/logout')
    client.post('/api/login', json={'username': 'admin', 'password': 'Admin@123'})
    deleted = client.delete(f'/api/projects/{project_id}')
    assert deleted.status_code == 200
    with app.app_context():
        assert db.session.get(Project, project_id) is None


def test_only_admin_can_create_workflow_steps(client):
    with app.app_context():
        project_id = db.session.scalar(db.select(Project.id))

    client.post('/api/login', json={'username': 'client', 'password': 'Client@123'})
    forbidden = client.post('/api/steps', json={
        'project_id': project_id,
        'title': 'Client-created step',
        'description': 'Should not be allowed',
    })
    assert forbidden.status_code == 403
    assert forbidden.get_json()['error'] == 'Admin role required'

    client.post('/api/logout')
    client.post('/api/login', json={'username': 'admin', 'password': 'Admin@123'})
    created = client.post('/api/steps', json={
        'project_id': project_id,
        'title': 'Admin-created step',
        'description': 'Allowed workflow step',
    })
    assert created.status_code == 201


def test_legacy_comment_statuses_are_normalized(client):
    from database.migrations import migrate_legacy_comment_schema

    with app.app_context():
        project = db.session.scalar(db.select(Project))
        step = db.session.scalar(db.select(WorkflowStep))
        client_user = db.session.scalar(db.select(User).where(User.role == 'client'))
        comment = Comment(
            project_id=project.id,
            step_id=step.id,
            client_id=client_user.id,
            body='Legacy status comment',
            status='Pending',
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        migrate_legacy_comment_schema()
        db.session.expire_all()
        assert db.session.get(Comment, comment_id).status == 'pending'


def test_comment_submission_and_memory_approval(client):
    login = client.post('/api/login', json={'username': 'client', 'password': 'Client@123'})
    assert login.status_code == 200

    step = WorkflowStep.query.first()
    comment_request = client.post('/api/comments', json={'step_id': step.id, 'body': 'Need a clearer requirement review'})
    assert comment_request.status_code == 201

    comment = Comment.query.first()
    assert comment.status == 'pending'

    client.post('/api/logout')
    admin_login = client.post('/api/login', json={'username': 'admin', 'password': 'Admin@123'})
    assert admin_login.status_code == 200

    review = client.put(f'/api/comments/{comment.id}/review', json={'status': 'accepted', 'admin_response': 'Good idea'})
    assert review.status_code == 200
    assert MemoryEntry.query.filter_by(source_comment_id=comment.id).count() == 1

    client.post('/api/logout')
    client.post('/api/login', json={'username': 'client', 'password': 'Client@123'})
    my_comments = client.get('/api/comments/my')
    accepted_comment = next(item for item in my_comments.get_json()['comments'] if item['id'] == comment.id)
    assert accepted_comment['status'] == 'accepted'
    assert accepted_comment['admin_response'] == 'Good idea'

    client.post('/api/logout')
    client.post('/api/login', json={'username': 'admin', 'password': 'Admin@123'})
    duplicate = client.put(f'/api/comments/{comment.id}/review', json={'status': 'accepted', 'admin_response': 'Again'})
    assert duplicate.status_code == 400

    client.post('/api/logout')
    client.post('/api/login', json={'username': 'client', 'password': 'Client@123'})
    second_comment = client.post('/api/comments', json={'step_id': step.id, 'body': 'This is a second suggestion'})
    assert second_comment.status_code == 201
    rejected_comment = Comment.query.filter_by(body='This is a second suggestion').first()

    client.post('/api/logout')
    client.post('/api/login', json={'username': 'admin', 'password': 'Admin@123'})
    reject_review = client.put(f'/api/comments/{rejected_comment.id}/review', json={'status': 'rejected', 'admin_response': 'Rejected'})
    assert reject_review.status_code == 200
    assert MemoryEntry.query.filter_by(source_comment_id=rejected_comment.id).count() == 0
