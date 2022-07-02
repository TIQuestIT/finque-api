from flask_restx import Api

from api.resources.customer import api_customer
from api.resources.home import api_home
from api.resources.user import api_role, api_user

api = Api(title="FinQue API", version="0.1", description="API for FinQue Project")

api.add_namespace(api_home, path="/")
api.add_namespace(api_user, path="/user")
api.add_namespace(api_role, path="/role")
api.add_namespace(api_customer, path="/customer")
