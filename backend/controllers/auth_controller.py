from flask import jsonify, request, session
from werkzeug.security import check_password_hash

from models.user import User


def login_user():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    session['user_id'] = user.id
    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200


def logout_user():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


def current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 401

    return jsonify({'user': user.to_dict()}), 200
