from typing import Tuple

from flask_restx import Namespace, Resource

api_home = Namespace("home", description="Home resource")


@api_home.route("/tea")
class Teapot(Resource):
    @classmethod
    def get(cls) -> Tuple[str, int]:
        return "I'm a teapot", 418
