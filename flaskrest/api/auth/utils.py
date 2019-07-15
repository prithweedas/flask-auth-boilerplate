import jwt
from datetime import datetime, timedelta
from flaskrest import app
from flask import request, jsonify, make_response
from flaskrest.api.auth.models import User
from functools import wraps


def create_token(user):
    token = jwt.encode({'id': user.id, 'exp': datetime.utcnow(
    ) + timedelta(minutes=1)}, app.config['SECRET_KEY'])
    refresh_token = jwt.encode({'id': user.id, 'exp': datetime.utcnow(
    ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return (token.decode('UTF-8'), refresh_token.decode('UTF-8'))


def check_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('x-access-token')
        new_token = None
        new_refresh_token = None
        if not token:
            return jsonify({'ok': False, 'error': 'Login Required'}), 401
        try:
            token_data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=token_data['id']).first()
        except jwt.ExpiredSignatureError:
            refresh_token = request.cookies.get('x-access-refresh-token')

            if not refresh_token:
                return jsonify({'ok': False, 'error': 'Login Required'}), 401

            try:
                token_data = jwt.decode(
                    refresh_token, app.config['SECRET_KEY'])
                current_user = User.query.filter_by(
                    id=token_data['id']).first()
            except jwt.ExpiredSignatureError:
                return jsonify({'ok': False, 'error': 'Login Required'}), 401
            print('refreshing...')
            new_token, new_refresh_token = create_token(current_user)
        except jwt.InvalidTokenError:
            return jsonify({'ok': False, 'error': 'Invalid Token'}), 401

        res = make_response(f(current_user, *args, **kwargs))
        if new_token and new_refresh_token:
            res.set_cookie("x-access-token", value=new_token)
            res.set_cookie("x-access-refresh-token", value=new_refresh_token)
        return res
    return wrapper
