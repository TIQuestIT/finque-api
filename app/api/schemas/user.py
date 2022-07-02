from api.models.user import RoleModel, RolesUsersModel, UserModel
from core.ma import ma
from marshmallow import fields


class RolesUsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RolesUsersModel
        dump_only = ("id",)
        inklude_fk = True
        include_relationships = True
        load_instance = True


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel
        dump_only = ("id",)
        inklude_fk = True
        include_relationships = True
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    # roles = fields.Nested(RolesUsersSchema, many=True)

    class Meta:
        model = UserModel
        dump_only = ("id",)
        load_only = ("password",)
        inklude_fk = True
        include_relationships = True
        load_instance = True
