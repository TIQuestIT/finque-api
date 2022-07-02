from typing import List
from uuid import uuid4

from core.db import db
from flask_security.core import RoleMixin, UserMixin


def _get_uuid():
    return uuid4().hex


class RolesUsersModel(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.String(), primary_key=True, default=_get_uuid)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("user.id"))
    role_id = db.Column("role_id", db.String(), db.ForeignKey("role.id"))

    @classmethod
    def find_by_id(cls, roles_users_id: str) -> "RolesUsersModel":
        return cls.query.filter_by(id=roles_users_id).first()

    @classmethod
    def find_by_user_id(cls, user_id: str) -> "RolesUsersModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_role_id(cls, role_id: str) -> "RolesUsersModel":
        return cls.query.filter_by(role_id=role_id).first()

    @classmethod
    def find_all(cls) -> List["RolesUsersModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        roles = self.roles
        UserModel.roles.append(roles)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class RoleModel(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.String(), primary_key=True, default=_get_uuid)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    @classmethod
    def find_by_role_id(cls, role_id: str) -> "RoleModel":
        return cls.query.filter_by(id=role_id).first()

    @classmethod
    def find_by_role_name(cls, name: str) -> "RoleModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["RoleModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class UserModel(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.String, primary_key=True, default=_get_uuid)
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
    def find_by_user_id(cls, user_id: str) -> "UserModel":
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
