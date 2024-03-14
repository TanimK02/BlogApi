from datetime import date
from flask import session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from db import db
from models import PostModel
from schemas import PostSchema
from decorators import login_and_authorization

blp = Blueprint("Posts", "posts", description="Operations on posts")


@blp.route("/create_post")
class MakePost(MethodView):
    @login_and_authorization(session, "poster")
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_data, admin_check=False):
        user_id = session.get("user_id")
        post_data["author_id"] = user_id
        post = PostModel(**post_data)
        try:
            db.session.add(post)
            db.session.commit()
        except SQLAlchemyError:
            abort(400, message="An error occurred while posting the item.")

        return post


@blp.route("/post/<int:post_id>")
class GetPost(MethodView):
    @blp.response(201, PostSchema)
    def get(self, post_id):
        post = db.get_or_404(PostModel, post_id)
        if post.published_at or post.author_id == session["user_id"]:
            return post
        else:
            abort(401, message="post not found")


@blp.route("/edit_post")
class EditPost(MethodView):
    @login_and_authorization(session, "poster")
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def put(self, post_data, admin_check=False):
        post = db.get_or_404(PostModel, post_data["id"])
        if "user_id" in session and session["user_id"] == post.author_id or admin_check:
            if post:
                try:
                    post_data["updated_at"] = date.today()
                    post.content = post_data["content"]
                    post.title = post_data.get("title") if not None else post.title
                    post.summary = post_data.get("summary") if not None else post.summary
                    db.session.add(post)
                    db.session.commit()
                    return post
                except SQLAlchemyError:
                    abort(500, message="An error occurred while editing the item.")
            else:
                abort(404, message="post not found")
        else:
            abort(401, message="not authorized")


@blp.route("/delete_post/<int:post_id>")
class PostDelete(MethodView):
    @login_and_authorization(session, "poster")
    def delete(self, post_id, admin_check=False):
        post = db.get_or_404(PostModel, post_id)
        if "user_id" in session and session["user_id"] == post.author_id or admin_check:
            try:
                db.session.delete(post)
                db.session.commit()
                return {"message": "Post deleted"}
            except SQLAlchemyError:
                abort(500, message="An error occurred while deleting the item.")
        else:
            abort(401, message="not authorized")


@blp.route("/publish_post")
class PostPublish(MethodView):
    @login_and_authorization(session, "poster")
    @blp.arguments(PostSchema)
    @blp.response(201, PostSchema)
    def post(self, post_data, admin_check=False):
        post = db.get_or_404(PostModel, post_data["id"])
        if "user_id" in session and session["user_id"] == post.author_id or admin_check:
            if post:
                try:
                    post_data["updated_at"] = date.today()
                    post.content = post_data["content"]
                    post.title = post_data.get("title") if not None else post.title
                    post.summary = post_data.get("summary") if not None else post.summary
                    post.published_at = date.today()
                    db.session.add(post)
                    db.session.commit()
                    return post
                except SQLAlchemyError:
                    abort(500, message="An error occurred while publishing the item.")
            else:
                abort(404, message="post not found")
        else:
            abort(401, message="not authorized")


@blp.route("/posts_list/<int:page>")
class PostList(MethodView):
    @login_and_authorization(session, "admin")
    @blp.response(200, PostSchema(many=True))
    def get(self, page):
        page -= 1
        page = page * 10
        try: 
            result = db.session.execute(
            db.select(PostModel).limit(10).offset(page).order_by(desc(PostModel.created_at))).scalars()
        except SQLAlchemyError:
            abort(400, message = "page not available")
        return result

@blp.route("/posts/<int:page>")
class PostList(MethodView):
    @blp.response(200, PostSchema(many=True))
    def get(self, page):
        page -= 1
        page = page * 10
        try:
            result = db.session.execute(db.select(PostModel).limit(10).offset(page). \
                                  filter(PostModel.published_at.isnot(None)).order_by(desc(PostModel.created_at))). \
            scalars()
        except SQLAlchemyError:
            abort(400, message = "page not available")
        return result
