from typing import Tuple

from flask_restx import Namespace, Resource

api = Namespace("home", description="Home resource")


@api.route("/tea")
class Teapot(Resource):
    @classmethod
    def get(cls) -> Tuple[str, int]:
        return "I'm a teapot", 418
