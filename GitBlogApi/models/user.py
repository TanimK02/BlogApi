
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    pic_url = db.Column(db.String())
    bio = db.Column(db.String())
    role = db.Column(db.Integer, db.ForeignKey("roles.id"), default=1)
    posts = db.relationship("PostModel", lazy='dynamic', cascade="all, delete")
    comments = db.relationship("CommentModel", lazy='dynamic', cascade="all, delete")
