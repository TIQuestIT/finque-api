from typing import Dict, Tuple

from flask_babel import gettext
from flask_restful import Resource
from models.customer import CustomerModel
from schemas.customer import CustomerSchema

customer_schema = CustomerSchema
customer_list_schema = CustomerSchema(many=True)


class Customer(Resource):
    @classmethod
    def get(cls, customer_number: int) -> Tuple[Dict, int]:
        customer = CustomerModel.find_by_customer_number(customer_number)

        if customer:
            return customer_schema.dump(customer), 200  # type: ignore

        return {"message": gettext("Customer not found.")}, 404

    @classmethod
    def post(cls, customer_number: int) -> Tuple[Dict, int]:
        customer = CustomerModel.find_by_customer_number(customer_number)

        if customer:
            return {"message": gettext("Customer already exists.")}, 400
