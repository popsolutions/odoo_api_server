from odoo import models, fields


class AuthJwtInheritValidator(models.Model):
    _inherit = "auth.jwt.validator"

    user_id_strategy = fields.Selection(
        selection_add=[("current_user", "Current User")],
        ondelete={"current_user": "set default"},
    )

    secret_config_parameter_check = fields.Boolean(
        "Check Secret Config Parameter", default=False
    )

    def get_validator_by_name(self, name):
        # lógica para encontrar o validador pelo nome
        return self.search([("name", "=", name)], limit=1)

    def _get_uid(self, payload):
        # Validate strategy current_user
        if self.user_id_strategy == "current_user":
            return (
                self.env["res.users"].search([("email", "=", payload.get("email"))]).id
            )
        return super()._get_uid(payload)

    def _get_partner_id(self, payload):
        # override for additional strategies
        if self.user_id_strategy == "current_user":
            user = self.env["res.users"].search([("email", "=", payload.get("email"))])
            return user.partner_id.id

        return super()._get_partner_id(payload)
