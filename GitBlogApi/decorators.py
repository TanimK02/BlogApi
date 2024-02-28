from db import db
from models import UserModel
from models import RoleModel
from flask_smorest import abort
import functools


def login_and_authorization(session, role="user"):
    def id_and_perm_check(func):
        @functools.wraps(func)
        def check(*args, **kwargs):
            if session.get("user_id"):
                query = db.one_or_404(db.select(UserModel).filter_by(id=session["user_id"]))
                role_name = db.one_or_404(db.select(RoleModel).filter_by(id=query.role))
                if role_name.role_name == role:
                    return func(*args, **kwargs)
                elif role_name.role_name == "admin":
                    return func(*args, **kwargs, admin_check=True)
                else:
                    abort(401, message="User does not have authorization for the task.")
            else:
                abort(404, message="Not a valid user id")
        return check
    return id_and_perm_check
