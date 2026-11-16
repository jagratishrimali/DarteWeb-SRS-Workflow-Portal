import pytest
from werkzeug.security import generate_password_hash

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
