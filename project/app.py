from flask import Flask
from flask_restx import Api

from config import DevelopmentConfig
from setup_db import db
from views import movie_ns, genres_ns, director_ns, auth_ns, user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)

app = create_app(DevelopmentConfig())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
