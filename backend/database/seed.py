from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User
from models.project import Project
from models.workflow import WorkflowStep


def seed_database():
    if User.query.count() > 0:
        return

    admin = User(username='admin', password_hash=generate_password_hash('Admin@123'), role='admin')
    client = User(username='client', password_hash=generate_password_hash('Client@123'), role='client')
    db.session.add_all([admin, client])
    db.session.commit()

    project = Project(
        name='Website Redesign Review',
        description='Review the website redesign workflow and project requirements.',
        srs_content='1. Prepare UX plan\n2. Define wireframes\n3. Implement front-end\n4. QA and signoff',
        review_status='published',
        client_id=client.id,
    )
    db.session.add(project)
    db.session.commit()

    step = WorkflowStep(
        project_id=project.id,
        title='Discovery',
        description='Gather requirements and agree on the scope of the redesign.',
        sequence=1,
    )
    db.session.add(step)
    db.session.commit()
