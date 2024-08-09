"""Controller to handle res.partner records."""

import json

from odoo.http import Controller, Response, request, route


class JWTResPartnerController(Controller):
    """Controller to handle res.partner records.
    - [GET] /res_partner: get all res.partner records.
    - [GET] /res_partner/<int:partner_id>: get a res.partner record by id.
    - [POST] /res_partner: create a res.partner record.
    """

    @route(
        "/api/res_partner",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_res_partner(self):
        """Get all res.partner records.
        - Return a JSON object with a list of res.partner records.
        """
        data = {}
        res_partner = request.env["res.partner"].with_user(request.env.uid).search([])
        data.update(
            res_partner=[
                {
                    "name": partner.name,
                    "email": partner.email,
                    "id": partner.id,
                    "cnpj": partner.vat,
                    "street": partner.street,
                    "street2": partner.street2,
                    "city": partner.city,
                    "state": {
                        "id": partner.state_id.id,
                        "name": partner.state_id.name,
                    },
                    "country": {
                        "id": partner.country_id.id,
                        "name": partner.country_id.name,
                    },
                    "is_company": partner.is_company,
                    "phone": partner.phone or "",
                }
                for partner in res_partner
            ]
        )
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/res_partner/<int:partner_id>",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_res_partner_by_id(self, partner_id):
        """Get a res.partner record by id.
        - Return a JSON object with the res.partner record.
        - Return a JSON object with an error if the res.partner record is not found.
        """
        data = {}
        res_partner = (
            request.env["res.partner"]
            .with_user(request.env.uid)
            .search([("id", "=", partner_id)])
        )
        if res_partner:
            data.update(
                res_partner={
                    "name": res_partner.name,
                    "email": res_partner.email,
                    "id": res_partner.id,
                    "address": res_partner.street or "N/A",
                    "phone": res_partner.phone or "N/A",
                }
            )
        else:
            data.update(error="Partner not found.")
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/res_partner",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["POST", "OPTIONS"],
    )
    def create_res_partner(self):
        """Create a res.partner record.
        - Return a JSON object with the created res.partner record.
        - Return a JSON object with an error if the name or email is missing.
        """
        data = {}
        raw_data = request.httprequest.get_data()
        post_data = json.loads(raw_data.decode("utf-8"))
        if "name" in post_data and "email" in post_data:
            res_partner = (
                request.env["res.partner"]
                .with_user(request.env.uid)
                .create(
                    {
                        "name": post_data["name"],
                        "email": post_data["email"],
                        "street": post_data.get("address", ""),
                        "phone": post_data.get("phone", ""),
                    }
                )
            )
            data.update(
                res_partner={
                    "name": res_partner.name,
                    "email": res_partner.email,
                    "id": res_partner.id,
                    "address": res_partner.street or "N/A",
                    "phone": res_partner.phone or "N/A",
                }
            )
        else:
            data.update(error="Missing name or email.")
        return Response(json.dumps(data), content_type="application/json", status=200)
