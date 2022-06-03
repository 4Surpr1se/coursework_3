import base64

SECRET_KEY = "you-will-never-guess"
JSON_AS_ASCII = False

ITEMS_PER_PAGE = 12

SQLALCHEMY_TRACK_MODIFICATIONS = False

ALGO = 'HS256'
TOKEN_EXPIRE_MINUTES = 15
TOKEN_EXPIRE_DAYS = 130

PWD_HASH_SALT = base64.b64decode("salt")
PWD_HASH_ITERATIONS = 100_000