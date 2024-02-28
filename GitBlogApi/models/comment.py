from db import db


class CommentModel(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    published_at = db.Column(db.String(), nullable=False)
    updated_at = db.Column(db.String(), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
