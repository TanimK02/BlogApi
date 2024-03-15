from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)