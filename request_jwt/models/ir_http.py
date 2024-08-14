"""Inherit HTTP. """
from odoo import models


class IrHttpJwtCustom(models.AbstractModel):
    """Inherit HttpJWT"""

    _inherit = "ir.http"

    @classmethod
    def _get_jwt_payload(cls, validator):
        """Obtain and validate the JWT payload from the request authorization header or
        cookie."""
        # Garantir que o super é chamado corretamente em um classmethod
        if validator.secret_config_parameter_check:
            token = cls._get_bearer_token()
            if not token:
                raise ValueError("Bearer token not found")
            secret = validator.env["ir.config_parameter"].get_param('jwt_secret')
            return validator._decode(token, secret)
        return super()._get_jwt_payload(validator)


