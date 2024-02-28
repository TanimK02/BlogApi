from db import db


class PostModel(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String())
    published_at = db.Column(db.String())
    status = db.Column(db.String())
    summary = db.Column(db.String())
    comments = db.relationship('CommentModel', lazy='dynamic', cascade="all, delete")
