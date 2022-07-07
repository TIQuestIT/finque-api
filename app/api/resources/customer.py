from typing import Any, Dict, Tuple

from api.models.customer import CustomerModel
from api.schemas.customer import CustomerSchema
from flask_babel import gettext
from flask_restx import Namespace, Resource, fields

api_customer = Namespace("customer", description="Customer resource")

customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)

customer_fields = api_customer.model(
    "Customer",
    {
        "customer_number": fields.Integer(required=True),
        "company": fields.String(required=True),
        "street": fields.String,
        "city": fields.String,
        "zip": fields.String,
        "url": fields.String,
        "mail": fields.String,
        "phone": fields.String,
    },
)


@api_customer.route("/")
class CustomerCollection(Resource):
    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        customers = customer_list_schema.dump(CustomerModel.find_all())
        return {"customers": [customer["company"] for customer in customers]}, 200

    @classmethod
    @api_customer.expect(customer_fields, skip_none=True)
    def post(cls) -> Tuple[Dict, int]:
        payload: Any = api_customer.payload

        if CustomerModel.find_by_customer_number(payload["customer_number"]):
            return {"message": gettext("Customer already exists.")}, 400

        customer = customer_schema.load(payload)
        try:
            customer.save_to_db()
        except Exception as e:
            print(e)
            return {
                "message": gettext("Error insterting customer"),
            }, 500
        return customer_schema.dump(customer), 201  # type: ignore


@api_customer.route("/<int:customer_number>")
class CustomerItem(Resource):
    @classmethod
    def get(cls, customer_number: int) -> Tuple[Dict, int]:
        customer = CustomerModel.find_by_customer_number(customer_number)

        if customer:
            return customer_schema.dump(customer), 200  # type: ignore

        return {"message": gettext("Customer not found.")}, 404

    @classmethod
    def delete(cls, customer_number: int) -> Tuple[Dict, int]:
        customer = CustomerModel.find_by_customer_number(customer_number)

        if customer is None:
            return {"message": gettext("Customer not found.")}, 404

        customer.delete_from_db()
        return {"message": gettext("Customer deleted.")}, 410

    @classmethod
    @api_customer.expect(customer_fields, skip_none=True)
    def put(cls, customer_number: int) -> Tuple[Dict, int]:
        payload: Dict[Any, Any] = api_customer.payload  # type: ignore

        customer = CustomerModel.find_by_customer_number(customer_number)

        if customer is None:
            return {"message": gettext("Customer not found.")}, 404

        for key, _ in payload.items():
            setattr(customer, key, payload[key])

        try:
            customer.save_to_db()
        except Exception as e:
            print(e)
            return {"message": gettext("Error updating customer")}, 500

        return customer_schema.dump(customer), 200  # type: ignore
