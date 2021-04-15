from flask import Blueprint

from .resources import UserAPI, UserTokenAPI, ProdutorAPI, LavouraAPI

user_view = UserAPI.as_view("user_api")
user_token_view = UserTokenAPI.as_view("user_token_api")
produtor_view = ProdutorAPI.as_view("produtor_api")
lavoura_view = LavouraAPI.as_view("lavoura_api")


def init_app(bp: Blueprint):
    bp.add_url_rule("/users/", view_func=user_view, methods=["POST"])
    bp.add_url_rule(
        "/user/token/", view_func=user_token_view, methods=["POST"]
    )
    bp.add_url_rule(
        "/produtores/",
        view_func=produtor_view,
        methods=["GET", "POST", "PATCH", "DELETE"],
    )
    bp.add_url_rule(
        "/lavouras/",
        view_func=lavoura_view,
        methods=["GET"],
    )
