from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_session import Session
from db import db
from resources.user import blp as UserBlueprint
from resources.post import blp as PostBlueprint
from resources.comments import blp as CommentBlueprint


def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "Blog REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.secret_key = "093903409089"
    app.config["SESSION_TYPE"] = "filesystem"

    db.init_app(app)
    Session(app)
    migrate = Migrate(app, db)
    api = Api(app)

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PostBlueprint)
    api.register_blueprint(CommentBlueprint)

    return app
