from flask import make_response, g
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

from app.db import get_db

parser = reqparse.RequestParser()
parser.add_argument('login', type=str)
parser.add_argument('password', type=str)


class ApiPing(Resource):
    def get(self):
        return {'api': 'pong'}


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['login']
        password = args['password']

        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            res = {'success': False}
        else:
            res = {
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': username
                }
            }
        resp = make_response(res)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def options(self):
        resp = make_response()
        resp.headers['Access-Control-Allow-Headers'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


class LoggedUser(Resource):
    def post(self):
        user = {
            'username': g.user['username'],
            'is_logged': True
        } if g.user else {'username': '', 'is_logged': False}
        resp = make_response(user)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    def options(self):
        resp = make_response()
        resp.headers['Access-Control-Allow-Headers'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
