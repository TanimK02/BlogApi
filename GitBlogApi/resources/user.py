from flask import session
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from decorators import login_and_authorization
from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Username already exists.")

        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="Email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            name=user_data["name"]
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = None

        if user_data.get("email", None):
            user = UserModel.query.filter(UserModel.email == user_data["email"]).first()
        elif user_data.get("username", None):
            user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            session["user_id"] = user.id
            return {"message": "logged in"}

        abort(401, message="Invalid credentials.")


@blp.route("/give_role/<int:user_id>/<int:role>")
class GiveUserRole(MethodView):
    @login_and_authorization(session, role="admin")
    @blp.response(200, UserSchema)
    def put(self, user_id, role, admin_check=False):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if user:
            user.role=role
            db.session.add(user)
            db.session.commit()
            return user
        else:
            abort(404, message="User not found")


@blp.route("/logout")
class UserLogout(MethodView):

    @login_and_authorization(session)
    def delete(self):
        session.clear()
        return {"message": "logged out."}


@blp.route("/delete_user/<int:user_id>")
class UserDelete(MethodView):

    @login_and_authorization(session)
    def delete(self, user_id, admin_check=False):
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if user:
            if session["user_id"] == user.id:
                db.session.delete(user)
                db.session.commit()
                return {"message": "user deleted"}
            else:
                abort(401, message="Not authorized")
        abort(400, message="Invalid user or not authorized")

