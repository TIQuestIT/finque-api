from typing import Any, Dict, Tuple

from api.models.user import (RoleModel, RolesUsersModel, UserModel,
                             user_datastore)
from api.schemas.user import RoleSchema, RolesUsersSchema, UserSchema
from core.logging import get_logger
from core.ma import ma
from flask_babel import gettext
from flask_restx import Namespace, Resource, fields
from flask_security.utils import encrypt_password, verify_password

logger = get_logger(__name__)

api_user = Namespace("user", description="User Ressource")
api_role = Namespace("role", description="Role Ressource")
api_rolesusers = Namespace("rolesusers", description="User assigned to Roles Resource")

user_schema = UserSchema()
user_list_schmea = UserSchema(many=True)
role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)
rolesusers_schema = RolesUsersSchema()
rolesusers_list_schema = RolesUsersSchema(many=True)

role_fields = api_role.model(
    "Role", {"name": fields.String(required=True), "description": fields.String}
)

user_fields = api_user.model(
    "User",
    {
        "email": fields.String(required=True),
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

rolesusers_fieds = api_rolesusers.model(
    "RolesUsers",
    {
        "user_id": fields.String,
        "role_id": fields.String,
    },
)


@api_user.route("/")
class UserCollection(Resource):
    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        users = user_list_schmea.dump(UserModel.find_all())
        return {"users": [user["username"] for user in users]}, 200

    @classmethod
    @api_user.expect(user_fields, skip_none=True)
    def post(cls) -> Tuple[Dict, int]:
        payload: Any = api_user.payload
        schema: UserSchema = user_schema.load(payload)
        data: Any = user_schema.dump(schema)

        user = user_datastore.find_user(username=data["username"])

        if user:
            return {"message": gettext("User already exists.")}, 400

        data["password"] = encrypt_password(payload.get("password"))

        user = user_datastore.create_user(**data)

        try:
            user_datastore.commit()  # type: ignore
        except Exception as e:
            logger.exception("Error creating user")
            return {"message": gettext("Error creating user.")}, 500

        return user_schema.dump(user), 201  # type: ignore


@api_user.route("/<string:username>")
class UserItem(Resource):
    @classmethod
    def get(cls, username) -> Tuple[Dict, int]:
        user = user_datastore.find_user(username=username)

        if user:
            return user_schema.dump(user), 200  # type: ignore

        return {"message": gettext("User not found.")}, 404

    @classmethod
    def delete(cls, username) -> Tuple[Dict, int]:
        user = user_datastore.find_user(username=username)

        if user is None:
            return {"message": gettext("User not found.")}, 404

        user_datastore.delete(user)
        user_datastore.commit()
        return {"message": gettext("User deleted.")}, 410


@api_role.route("/")
class RoleCollection(Resource):
    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        roles = role_list_schema.dump(RoleModel.find_all())
        return {"roles": [role["name"] for role in roles]}, 200

    @classmethod
    @api_role.expect(role_fields, skip_none=True)
    def post(cls) -> Tuple[Dict, int]:
        payload: Any = api_user.payload
        schema: RoleSchema = role_schema.load(payload)
        data: Any = role_schema.dump(schema)

        role = user_datastore.find_role(data["name"])

        if role:
            return {"message": gettext("Role already exists.")}, 400

        try:
            user_datastore.create_role(**data)
            user_datastore.commit()
        except Exception as e:
            logger.exception("Error addin role")
            return {"message": gettext("Error adding role.")}, 500

        return role_schema.dump(role), 201  # type: ignore


@api_role.route("/<string:name>")
class RoleItem(Resource):
    @classmethod
    def get(cls, name: str) -> Tuple[Dict, int]:
        role = user_datastore.find_role(name)

        if role is None:
            return {"message": gettext("Role not found.")}, 404

        return role_schema.dump(role), 200  # type: ignore


@api_rolesusers.route("/<string:user_id>")
class RoleUsersUserCollection(Resource):
    @classmethod
    def get(cls, user_id: str):
        users = RolesUsersModel.find_by_user_id(user_id=user_id)

        if users is None:
            return {"message": gettext("Users not found.")}

        return rolesusers_schema.dump(users), 200  # type: ignore
