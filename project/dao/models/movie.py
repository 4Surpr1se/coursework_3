from project.dao.models.base import BaseMixin
from project.setup_db import db
from sqlalchemy.orm import relationship


class Movie(BaseMixin, db.Model):
    __tablename__ = "movies"

    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))

    def __repr__(self):
        return f"<Movie '{self.name.title()}'>"
