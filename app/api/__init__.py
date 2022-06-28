from flask_restx import Api

from api.resources.customer import api as customer
from api.resources.home import api as home

api = Api(title="FinQue API", version="0.1", description="API for FinQue Project")

api.add_namespace(home, path="/")
api.add_namespace(customer, path="/customer")
