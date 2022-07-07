from uuid import uuid4

from core.db import db
from flask_security.core import RoleMixin, UserMixin
from flask_security.datastore import SQLAlchemyUserDatastore


def _get_uuid():
    return uuid4().hex


class RolesUsersModel(db.Model):
    __tablename__ = "roles_users"
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True
    )
    role_id = db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True
    )


class RoleModel(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    @classmethod
    def find_all(cls):
        return cls.query.all()


class UserModel(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, default=_get_uuid)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "RoleModel",
        secondary="roles_users",
        backref=db.backref("users", lazy="dynamic"),
    )

    @classmethod
    def find_all(cls):
        return cls.query.all()


user_datastore = SQLAlchemyUserDatastore(db, UserModel, RoleModel)
