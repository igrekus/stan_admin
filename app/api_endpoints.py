import json

from flask import make_response, g, request
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

from app.db import get_db

parser = reqparse.RequestParser()
parser.add_argument('login', type=str)
parser.add_argument('password', type=str)


class ApiPing(Resource):
    def get(self):
        return {'api': 'pong'}

    def post(self):

        data = json.loads(request.data)
        print(data)

        data['result'] = 'success'
        resp = make_response(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        # {'clientType': 'Юр. лицо', 'legalForm': 'АО', 'clientName': 'Техно-строй', 'personalTaxNum': '1234567890',
        #  'ogrnNum': '0987654321', 'legalAddr': 'Москва, Сущёвский вал, 10', 'actualAddr': 'Москва, Сущёвский вал, 10',
        #  'buildingPurpose': 'ФОК', 'buildingNote': 'стадион на 1000 мест', 'contactName': 'Иванов И.И.',
        #  'contactPhone': '+7 (999) 123-45-67', 'contactJob': 'менеджер проекта',
        #  'contactEmail': 'manager-ivan@fok-42.ru'}
        return resp

    def options(self):
        resp = make_response()
        resp.headers['Access-Control-Allow-Headers'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,OPTIONS'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


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
