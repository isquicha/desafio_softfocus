from flask import request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from src.utils import json_response
from src.models import ProdutorRural, Lavoura
from src.extensions.database import db
from src.extensions.authentication import (
    create_user,
    generate_token,
    token_required,
    AlreadyRegisteredError,
    InvalidUserError,
    IncorrectPasswordError,
)


class UserAPI(MethodView):
    @token_required
    def post(self, **kwargs):
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="You must provide a json body"
            )

        username = body.get("username", None)
        password = body.get("password", None)
        name = body.get("name", None)

        if username is None:
            return json_response(
                status_code=400, message="Field 'username' must not be empty"
            )
        if password is None:
            return json_response(
                status_code=400, message="Field 'password' must not be empty"
            )

        try:
            user = create_user(username=username, password=password, name=name)
            payload = {
                "id": user.id,
                "username": user.username,
                "name": user.name,
            }
            return json_response(status_code=201, payload=payload)
        except AlreadyRegisteredError:
            return json_response(
                status_code=400,
                message=f"Username {username} is already registered",
            )
        except Exception:
            return json_response(
                status_code=500, message="Could not create user"
            )


class UserTokenAPI(MethodView):
    def post(self):
        """Tries to get user's access token"""
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="A JSON body must be provided"
            )

        username = body.get("username", None)
        password = body.get("password", None)

        if username is None:
            return json_response(
                status_code=400, message="Field 'username' must not be empty"
            )
        if password is None:
            return json_response(
                status_code=400, message="Field 'password' must not be empty"
            )

        try:
            token = generate_token(username=username, password=password)
        except (InvalidUserError, IncorrectPasswordError):
            return json_response(
                # ! Don't say to hackers if it is the username that doesn't
                # ! exists or if the password is incorrect.
                status_code=400,
                message="Invalid username or password",
            )
        else:
            return json_response(
                message="Token successful generated",
                payload={"access_token": token},
            )


class ProdutorAPI(MethodView):
    @token_required
    def get(self, **kwargs):
        cpf = request.args.get("cpf", None)
        if cpf:
            produtores = ProdutorRural.query.filter(
                ProdutorRural.cpf.like("%" + cpf + "%")
            ).all()
        else:
            produtores = ProdutorRural.query.all()

        return json_response(
            payload={
                "produtores": [
                    {
                        "nome": produtor.nome,
                        "cpf": produtor.cpf,
                        "email": produtor.email,
                    }
                    for produtor in produtores
                ]
            }
        )

    @token_required
    def post(self, **kwargs):
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="You must provide a json body"
            )

        nome = body.get("nome", None)
        email = body.get("email", None)
        cpf = body.get("cpf", None)

        if nome is None:
            return json_response(
                status_code=400, message="Field 'nome' must not be empty"
            )
        if email is None:
            return json_response(
                status_code=400, message="Field 'email' must not be empty"
            )
        if cpf is None:
            return json_response(
                status_code=400, message="Field 'cpf' must not be empty"
            )

        try:
            produtor = ProdutorRural(nome=nome, email=email, cpf=cpf)
            db.session.add(produtor)
            db.session.commit()
        except IntegrityError:
            return json_response(
                status_code=400, message="CPF already registered"
            )
        except Exception:
            return json_response(status_code=500, message="Could not create")

        return json_response(201)

    @token_required
    def patch(self, **kwargs):
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="You must provide a json body"
            )

        novo_nome = body.get("novo_nome", None)
        novo_email = body.get("novo_email", None)
        novo_cpf = body.get("novo_cpf", None)
        cpf = body.get("cpf", None)

        if cpf is None:
            return json_response(
                status_code=400, message="Field 'cpf' must not be empty"
            )

        if novo_nome is None and novo_email is None and novo_cpf is None:
            return json_response(
                status_code=400,
                message=(
                    "You must provide at least one of those fields:"
                    " 'novo_nome', 'novo_email', 'novo_cpf'"
                ),
            )

        produtor = ProdutorRural.query.filter_by(cpf=cpf).first()

        if not produtor:
            return json_response(
                status_code=404,
                message=f"Produtor with cpf {cpf} was not found",
            )
        if novo_cpf:
            produtor.cpf = novo_cpf
        if novo_email:
            produtor.email = novo_email
        if novo_nome:
            produtor.nome = novo_nome

        try:
            db.session.add(produtor)
            db.session.commit()
        except IntegrityError:
            return json_response(
                status_code=400, message="CPF already registered"
            )
        except Exception:
            return json_response(status_code=500, message="Could not update")

        return json_response(200)

    @token_required
    def delete(self, **kwargs):
        body = request.get_json()
        if body is None:
            return json_response(
                status_code=400, message="You must provide a json body"
            )

        cpf = body.get("cpf", None)

        if cpf is None:
            return json_response(
                status_code=400, message="Field 'cpf' must not be empty"
            )

        produtor = ProdutorRural.query.filter_by(cpf=cpf).first()
        if not produtor:
            return json_response(
                status_code=404,
                message=f"Produtor with cpf {cpf} was not found",
            )

        try:
            db.session.delete(produtor)
            db.session.commit()
        except Exception:
            return json_response(status_code=500, message="Could not delete")
        return json_response(200)


class LavouraAPI(MethodView):
    @token_required
    def get(self, **kwargs):
        return json_response(
            payload={
                "lavouras": [
                    {
                        "latitude": lavoura.latitude,
                        "longitude": lavoura.longitude,
                        "tipo": lavoura.tipo,
                    }
                    for lavoura in Lavoura.query.all()
                ]
            }
        )
