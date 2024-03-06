from db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class RoleModel(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(unique=True, nullable=False)