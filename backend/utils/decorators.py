from functools import wraps
from flask import session, jsonify


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return fn(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = None
            from models.user import User
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
            if not user or user.role not in roles:
                required_roles = ', '.join(roles)
                return jsonify({'error': f'{required_roles.capitalize()} role required'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
