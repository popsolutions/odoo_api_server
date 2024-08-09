"""Main controller for JWT authentication."""

import time
import json
import jwt

from odoo.http import Controller, Response, request, route

VALIDATOR_NAME = "api"


class JWTLoginController(Controller):
    """Controller to handle JWT authentication.
    - [GET] /auth_jwt: login endpoint
    - [GET] /auth_jwt/whoami: whoami endpoint
    """

    @route(
        "/api/auth_jwt",
        type="http",
        auth="public",
        cors="*",
        save_session=False,
        csrf=False,
        methods=["POST"],
    )
    def login(self):
        """Login endpoint.
        - Request body must be a JSON object with "login" and "password" keys.
        - If login and password are correct, return a JSON object with a JWT token.
        - If login or password are missing, return a JSON object with an error.
        - If login or password are incorrect, return a JSON object with an error.
        """
        data = {}
        try:
            raw_data = request.httprequest.get_data()
            post_data = json.loads(raw_data.decode("utf-8"))

            if "login" in post_data and "password" in post_data:
                login = post_data["login"]
                password = post_data["password"]
                uid = request.session.authenticate(request.session.db, login, password)
                if uid is None:
                    return Response(
                        json.dumps({"error": "Invalid login or password."}),
                        content_type="application/json",
                        status=401,
                    )
                # Get validator
                validator = request.env["auth.jwt.validator"]._get_validator_by_name(
                    VALIDATOR_NAME
                )
                # Get Secret key
                secret = validator.secret_key
                if validator.secret_config_parameter_check:
                    secret = (
                        request.env["ir.config_parameter"]
                        .sudo()
                        .get_param("jwt_secret")
                    )

                # Get Expiration
                expiration = int(
                    request.env["ir.config_parameter"]
                    .sudo()
                    .get_param("jwt_expiration", "3600")
                )
                # Set Payload
                payload = {
                    "user_id": uid,
                    "email": login,
                }
                # Generate Token
                token = validator._encode(payload, secret, expiration)
                data.update(token=token)
            else:
                data.update(error="Missing email or password.")
        except Exception as e:
            data.update(error=str(e))

        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/auth_jwt/whoami",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def whoami(self):
        """Whoami endpoint.
        - Return a JSON object with the user name and email if the user is authenticated.
        - Return a JSON object with an error if the user is not authenticated.
        """
        data = {}
        if getattr(request, "jwt_partner_id", None):
            partner = request.env["res.partner"].browse(request.jwt_partner_id)
            data.update(name=partner.name, email=partner.email, uid=request.env.uid)
        return Response(json.dumps(data), content_type="application/json", status=200)

