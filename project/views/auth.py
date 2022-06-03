from flask import request
from flask_restx import Resource, Namespace

from project.implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return "", 201


@auth_ns.route('/login')
class AuthVieww(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get("email")
        password = req_json.get("password")
        user = user_service.check_login(email, password)
        return user

    def put(self):
        req_json = request.json
        return user_service.new_tokens(req_json)
