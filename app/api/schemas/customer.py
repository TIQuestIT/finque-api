from api.models.customer import CustomerModel
from core.ma import ma


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True
