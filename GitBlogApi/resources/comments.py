from datetime import date
from flask import session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from db import db
from models import CommentModel, PostModel
from schemas import CommentSchema
from decorators import login_and_authorization

blp = Blueprint("Comments", "comments", description="Operations on comments")


@blp.route("/add_comment")
class CommentAdd(MethodView):

    @login_and_authorization(session)
    @blp.arguments(CommentSchema)
    @blp.response(201)
    def post(self, comment_data):
        user_id = session.get("user_id")
        comment_data["author_id"] = user_id
        comment_data["published_at"] = date.today()
        comment = CommentModel(**comment_data)
        try:
            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding the comment.")

        return {"message": "Created comment"}


@blp.route("/edit_comment")
class EditComment(MethodView):

    @login_and_authorization(session)
    @blp.arguments(CommentSchema)
    @blp.response(201, CommentSchema)
    def put(self, comment_data, admin_check=False):
        comment = db.get_or_404(CommentModel, comment_data["id"])
        if "user_id" in session and session["user_id"] == comment.author_id or admin_check:
            if comment:
                try:
                    comment_data["updated_at"] = date.today()
                    comment.content = comment_data["content"]
                    db.session.add(comment)
                    db.session.commit()
                    return comment
                except SQLAlchemyError:
                    abort(500, message="An error occurred while editing the comment.")
            else:
                abort(404, message="comment not found")
        else:
            abort(401, message="not authorized")


@blp.route("/delete_comment/<int:comment_id>")
class CommentDelete(MethodView):
    @login_and_authorization(session)
    def delete(self, comment_id, admin_check=False):
        comment = db.get_or_404(CommentModel, comment_id)
        if "user_id" in session and session["user_id"] == comment.author_id or admin_check:
            try:
                db.session.delete(comment)
                db.session.commit()
                return {"message": "Comment deleted"}
            except SQLAlchemyError:
                abort(500, message="An error occurred while deleting the comment.")
        else:
            abort(401, message="not authorized")


@blp.route("/load_comment/<int:post_id>/<int:rows>")
class CommentLoad(MethodView):

    @blp.response(200, CommentSchema(many=True))
    def get(self, post_id, rows):
        rows = rows - 1
        rows = rows * 10
        comments = db.get_or_404(PostModel, post_id).comments.order_by(desc(CommentModel.published_at)).limit(10).\
            offset(rows)
        return comments.all()
