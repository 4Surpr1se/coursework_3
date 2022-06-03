import base64
import hashlib
import hmac
import calendar
import datetime

import jwt
from flask_restx import abort

from project.container import PWD_HASH_SALT, PWD_HASH_ITERATIONS, TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGO
from project.dao.user import UserDAO


class UsersService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create(self, new_user):
        new_user["password"] = self.make_user_password_hash(new_user.get("password"))
        if new_user.get("name") is None:
            new_user["name"] = None
        if new_user.get("surname") is None:
            new_user["surname"] = None
        if new_user.get("favorite_genre") is None:
            new_user["favorite_genre"] = None

        return self.dao.create(new_user)

    def make_user_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_password(self, password_hash, other_password):
        hash_decoded = base64.b64decode(password_hash)

        other_hash = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(hash_decoded, other_hash)

    def check_login(self, email, password):
        user = self.dao.user_by_email(email)

        if user is None:
            raise abort(484)

        if not self.compare_password(user.password, password):
            raise abort(484)

        data = {
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "favorite_genre": user.favorite_genre
        }

        response_ans = {"access_token": self.create_acces_token(data), "refresh_token": self.create_refresh_token(data)}

        return response_ans

    def create_acces_token(self, data):
        minutes = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        data["exp"] = calendar.timegm(minutes.timetuple())
        return jwt.encode(data, SECRET_KEY, algorithm=ALGO)

    def check_access_token(self, access_token):
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGO)
            return payload
        except Exception as e:
            return False

    def create_refresh_token(self, data):
        days = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days.timetuple())
        return jwt.encode(data, SECRET_KEY, algorithm=ALGO)


    def check_refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGO)
            return payload
        except Exception as e:
            return False

    def new_tokens(self, data):
        if self.check_access_token(data.get("access_token")) is not False and self.check_refresh_token(data.get("refresh_token")) is not False:
            payload = self.check_refresh_token(data.get("refresh_token"))

            data_to_send = {
                "email": payload.get("email"),
                "name": payload.get("name"),
                "surname": payload.get("surname"),
                "favorite_genre": payload.get("favorite_genre")
                        }

            response_ans = {"access_token": self.create_acces_token(data_to_send),
                            "refresh_token": self.create_refresh_token(data_to_send)}

            return response_ans
        else:
            return 'no permission'

    def all_info_about_user(self, token):
        data = self.check_access_token(token)
        return self.dao.user_by_email(data["email"])

    def patch(self, new_data, user_data):
        if new_data.get("email") is None:
            new_data["email"] = user_data.email
        if new_data.get("name") is None:
            new_data["name"] = user_data.name
        if new_data.get("surname") is None:
            new_data["surname"] = user_data.surname
        if new_data.get("favorite_genre") is None:
            new_data["favorite_genre"] = user_data.favorite_genre
        new_data["id"] = user_data.id
        return self.dao.update(new_data)

    def password_change(self, password_1, password_2, user):
        if self.check_login(user.email, password_1):
            password_2 = self.make_user_password_hash(password_2)
            self.dao.password_change(user, password_2)
            return "password changed"
        else:
            return "wrong password"
