import os

from flask import Flask
from flask_cors import CORS

from config import INSTANCE_DIR, SECRET_KEY, SQLALCHEMY_DATABASE_URI
from extensions import db


def create_app():
    from database.seed import seed_database

    os.makedirs(INSTANCE_DIR, exist_ok=True)
    app = Flask(__name__)
    app.config.from_object('config')
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    CORS(app, supports_credentials=True, resources={r'/api/*': {'origins': 'http://localhost:5173'}})

    from models.user import User
    from models.project import Project
    from models.workflow import WorkflowStep
    from models.comment import Comment
    from models.memory import MemoryEntry

    with app.app_context():
        db.create_all()
        seed_database()

    from routes.auth_routes import auth_bp
    from routes.project_routes import project_bp
    from routes.workflow_routes import workflow_bp
    from routes.comment_routes import comment_bp
    from routes.memory_routes import memory_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(workflow_bp, url_prefix='/api')
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(memory_bp, url_prefix='/api')

    @app.get('/api/health')
    def health_check():
        return {'status': 'ok'}

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
