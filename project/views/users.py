from flask import request
from flask_restx import Resource, Namespace, abort

from project.implemented import user_service
from project.schemas.user import UserSchema

user_ns = Namespace('user')


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        if user_service.check_access_token(token):
            return func(*args, **kwargs)
        else:
            print("JWT Decode Exception")
            abort(401)
            return "no permission"

    return wrapper


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user = user_service.all_info_about_user(token)
        return UserSchema().dump(user), 200

    @auth_required
    def patch(self):
        req_json = request.json
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user = user_service.all_info_about_user(token)
        new_user = user_service.patch(req_json, user)
        return UserSchema().dump(new_user), 200


@user_ns.route('/password')
class UserView(Resource):
    @auth_required
    def put(self):
        password_1 = request.json.get("password_1")
        password_2 = request.json.get("password_2")
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user = user_service.all_info_about_user(token)
        return user_service.password_change(password_1, password_2, user)
