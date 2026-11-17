from sqlalchemy import inspect, text
from sqlalchemy.dialects.mysql import ENUM

from extensions import db


def migrate_legacy_comment_schema():
    inspector = inspect(db.engine)
    if 'comments' not in inspector.get_table_names():
        return

    comment_columns = {column['name']: column for column in inspector.get_columns('comments')}
    if 'status' in comment_columns:
        if isinstance(comment_columns['status']['type'], ENUM):
            with db.engine.begin() as connection:
                connection.execute(text(
                    "ALTER TABLE comments MODIFY status VARCHAR(20) NOT NULL DEFAULT 'pending'"
                ))

        with db.engine.begin() as connection:
            connection.execute(text(
                "UPDATE comments SET status = LOWER(status) "
                "WHERE LOWER(status) IN ('pending', 'accepted', 'rejected')"
            ))

    if db.engine.dialect.name != 'mysql':
        return

    if 'project_id' not in comment_columns:
        with db.engine.begin() as connection:
            connection.execute(text('ALTER TABLE comments ADD COLUMN project_id INTEGER NULL'))

    with db.engine.begin() as connection:
        connection.execute(text(
            'UPDATE comments AS c '
            'JOIN workflow_steps AS s ON s.id = c.step_id '
            'SET c.project_id = s.project_id '
            'WHERE c.project_id IS NULL'
        ))

        missing_project_count = connection.execute(text(
            'SELECT COUNT(*) FROM comments WHERE project_id IS NULL'
        )).scalar_one()
        if missing_project_count:
            raise RuntimeError(
                f'Cannot migrate comments: {missing_project_count} comment(s) have no matching workflow step.'
            )

        if 'project_id' not in comment_columns or comment_columns['project_id']['nullable']:
            connection.execute(text(
                'ALTER TABLE comments MODIFY project_id INTEGER NOT NULL'
            ))

        foreign_keys = inspector.get_foreign_keys('comments')
        has_project_foreign_key = any(
            key.get('constrained_columns') == ['project_id']
            and key.get('referred_table') == 'projects'
            for key in foreign_keys
        )
        if not has_project_foreign_key:
            connection.execute(text(
                'ALTER TABLE comments '
                'ADD CONSTRAINT fk_comments_project_id_projects '
                'FOREIGN KEY (project_id) REFERENCES projects (id)'
            ))
