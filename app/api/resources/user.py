from typing import Any, Dict, Tuple

from api.models.user import RoleModel, RolesUsersModel, UserModel
from api.schemas.user import RoleSchema, RolesUsersSchema, UserSchema
from flask_babel import gettext
from flask_restx import Namespace, Resource, fields

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
        "roles": fields.List(fields.Nested(role_schema, skip_none=True)),
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
        user = UserModel.find_by_username(payload["username"])

        if user:
            return {"message": gettext("User already exists.")}, 400

        user = user_schema.load(payload)

        try:
            user.save_to_db()
        except Exception as e:
            print(e)
            return {"message": gettext("Error inserting user.")}, 500

        return user_schema.dump(payload), 201  # type: ignore


@api_user.route("/<string:user_id>")
class UserItem(Resource):
    @classmethod
    def get(cls, user_id) -> Tuple[Dict, int]:
        user = UserModel.find_by_user_id(user_id)

        if user:
            return user_schema.dump(user), 200  # type: ignore

        return {"message": gettext("User not found.")}, 404

    @classmethod
    def delete(cls, user_id) -> Tuple[Dict, int]:
        user = UserModel.find_by_user_id(user_id)

        if user is None:
            return {"message": gettext("User not found.")}, 404

        user.delete_from_db()
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
        payload: Any = api_role.payload
        role = RoleModel.find_by_role_name(payload["name"])

        if role:
            return {"message": gettext("Role already exists.")}, 400

        role = role_schema.load(payload)

        try:
            role.save_to_db()
        except Exception as e:
            print(e)
            return {"message": gettext("Error inserting role.")}, 500

        return role_schema.dump(role), 201  # type: ignore


@api_role.route("/<string:name>")
class RoleItem(Resource):
    @classmethod
    def get(cls, name: str) -> Tuple[Dict, int]:
        role = RoleModel.find_by_role_name(name)

        if role is None:
            return {"message": gettext("Role not found.")}, 404

        return role_schema.dump(role), 200  # type: ignore

    @classmethod
    def delete(cls, name: str) -> Tuple[Dict, int]:
        role = RoleModel.find_by_role_name(name)

        if role is None:
            return {"message": gettext("Role not found.")}, 404

        role.delete_from_db()

        return {"message": gettext("Role deleted successfully.")}, 200


@api_rolesusers.route("/<string:user_id>")
class RoleUsersUser(Resource):
    @classmethod
    def get(cls, user_id: str):
        users = RolesUsersModel.find_by_user_id(user_id=user_id)

        if users is None:
            return {"message": gettext("Users not found.")}
