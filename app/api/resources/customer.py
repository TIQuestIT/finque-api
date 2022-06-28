from typing import Any, Dict, Tuple

from api.models.customer import CustomerModel
from api.schemas.customer import CustomerSchema
from flask import jsonify, request
from flask_babel import gettext
from flask_restx import Namespace, Resource, fields

api = Namespace("customer", description="Customer resource")

customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)

customer_fields = api.model(
    "Resource",
    {
        "customer_number": fields.Integer,
        "company": fields.String,
        "street": fields.String(default=""),
        "city": fields.String(default=""),
        "zip": fields.String(default=""),
        "url": fields.String(default=""),
        "mail": fields.String(default=""),
        "phone": fields.String(default=""),
    },
)


@api.route("/")
class CustomerCollection(Resource):
    @classmethod
    def get(cls) -> Tuple[Dict, int]:
        customers = customer_list_schema.dump(CustomerModel.find_all())
        return {"customers": [customer["company"] for customer in customers]}, 200

    @classmethod
    @api.expect(customer_fields)
    def post(cls) -> Tuple[Dict, int]:
        payload: Any = api.payload

        customer = CustomerModel.find_by_customer_number(payload["customer_number"])
        if customer:
            return {"message": gettext("Customer already exists.")}, 400

        customer = customer_schema.load(payload)
        try:
            customer.save_to_db()
        except Exception as e:
            print(e)
            return {
                "message": gettext("Error insterting customer"),
            }, 500
        return customer_schema.dump(customer), 201


@api.route("/<int:customer_number>")
class CustomerItem(Resource):
    @classmethod
    def get(cls, customer_number: int) -> Tuple[Dict, int]:
        customer = CustomerModel.find_by_customer_number(customer_number)

        if customer:
            return customer_schema.dump(customer), 200  # type: ignore

        return {"message": gettext("Customer not found.")}, 404
