from ma import ma
from models.customer import CustomerModel


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerModel
        # load_only = ()
        dump_only = ("id",)
        include_fk = True
        load_instance = True
