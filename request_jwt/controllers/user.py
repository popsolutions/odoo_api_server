"""Main controller for JWT authentication."""

import json
from odoo.tools import json_default
from odoo.http import Controller, Response, request, route
from odoo.exceptions import ValidationError


VALIDATOR_NAME = "api"


class JWTLoginController(Controller):
    """Controller to handle JWT authentication."""

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
        """Login endpoint."""
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
                
                validator = request.env["auth.jwt.validator"]._get_validator_by_name(
                    VALIDATOR_NAME
                )
                if not validator:
                    return Response(
                        json.dumps({"error": "Validator not found."}),
                        content_type="application/json",
                        status=500,
                    )

                secret = validator.secret_key
                if validator.secret_config_parameter_check:
                    secret = request.env["ir.config_parameter"].sudo().get_param("jwt_secret")
                if not secret:
                    return Response(
                        json.dumps({"error": "JWT secret not configured."}),
                        content_type="application/json",
                        status=500,
                    )

                expiration = int(
                    request.env["ir.config_parameter"]
                    .sudo()
                    .get_param("jwt_expiration", "3600")
                )

                payload = {
                    "user_id": uid,
                    "email": login,
                    "role": "admin",
                }
                token = validator._encode(payload, secret, expiration)
                data.update(token=token)
            else:
                return Response(
                    json.dumps({"error": "Missing login or password."}),
                    content_type="application/json",
                    status=400,
                )
        except Exception as e:
            data.update(error=str(e))
            return Response(json.dumps(data), content_type="application/json", status=500)

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
        """Whoami endpoint."""
        data = {}
        if getattr(request, "jwt_partner_id", None):
            partner = request.env["res.partner"].browse(request.jwt_partner_id)
            data.update(name=partner.name, email=partner.email, uid=request.env.uid)
        else:
            data.update(error="User not authenticated.")
            return Response(json.dumps(data), content_type="application/json", status=401)
        
        return Response(json.dumps(data), content_type="application/json", status=200)

    # Outras rotas devem ser revisadas de maneira similar...

