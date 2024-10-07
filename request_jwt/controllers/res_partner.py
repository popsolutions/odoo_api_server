"""Controller to handle res.partner records."""

import json
import logging
from odoo.http import Controller, Response, request, route

_logger = logging.getLogger(__name__)

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
        user = request.env.user
        team_ids = user.sale_team_ids.ids if hasattr(user, 'sale_team_ids') else [user.sale_team_id.id]
        res_partner = request.env["res.partner"].with_user(request.env.uid).search([
                ("team_id", "in", team_ids)
            ])
        data.update(
            res_partner=[
                {
                    "name": partner.name,
                    "email": partner.email,
                    "id": partner.id,
                    "cnpj": partner.cnpj_cpf,
                    "street": partner.street,
                    "city": partner.city,
                    "zip": partner.zip,
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
                    "cnpj": partner.cnpj,
                    "street": partner.street,
                    "city": partner.city,
                    "state": {
                        "id": partner.state_id.id,
                        "name": partner.state_id.name,
                    },
                    "country": {
                        "id": partner.country_id.id,
                        "name": partner.country_id.name,
                    },
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
            res_partner_check = (
                request.env["res.partner"]
                .with_user(request.env.uid)
                .search([("id", "=", post_data["id"])])
            )
            if res_partner_check:
                res_partner = (
                    request.env["res.partner"]
                    .with_user(request.env.uid)
                    .update(
                        {
                            "name": post_data["name"],
                            "email": post_data["email"],
                            "cnpj_cpf":  post_data["cnpj"],
                            "is_company": True,
                            "street": post_data.get("street", ""),
                            "city": post_data.get("city", ""), 
                            "phone": post_data.get("phone", ""),
                        }
                    )
                )
                data.update(
                    res_partner={
                        "name": res_partner.name,
                        "email": res_partner.email,
                        "cnpj_cpf":  post_data["cnpj"],
                        "is_company": True,
                        "id": res_partner.id,
                        "street": post_data.get("street", ""),
                        "city": post_data.get("city", ""), 
                        "phone": post_data.get("phone", ""),
                    }
                )   
 
            else:
                res_partner = (
                    request.env["res.partner"]
                    .with_user(request.env.uid)
                    .create(
                        {
                            "name": post_data["name"],
                            "email": post_data["email"],
                            "cnpj_cpf":  post_data["cnpj"],
                            "is_company": True,
                            "street": post_data.get("street", ""),
                            "city": post_data.get("city", ""), 
                            "phone": post_data.get("phone", ""),
                        }
                    )
                )
                data.update(
                    res_partner={
                        "name": res_partner.name,
                        "email": res_partner.email,
                        "cnpj_cpf":  post_data["cnpj"],
                        "is_company": True,
                        "id": res_partner.id,
                        "street": post_data.get("street", ""),
                        "city": post_data.get("city", ""), 
                        "phone": post_data.get("phone", ""),
                    }
                )   
        else:
            data.update(error="Missing name or email.")
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/res_partner/coutry/<int:country_id>/state/<int:state_id>/cities",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_cities_by_country_and_state(self, country_id, state_id):
        """Get a list of cities for the specified country_id and state_id."""
        if not country_id or not state_id:
            return Response(
                json.dumps({"error": "country_id and state_id are required"}),
                content_type="application/json",
                status=400,
            )
        
        res_partners = request.env["res.partner"].with_user(request.env.uid).search([
            ('country_id', '=', int(country_id)),
            ('state_id', '=', int(state_id))
        ])
      
        cities = list(set(partner.city for partner in res_partners if partner.city))
        
        return Response(
            json.dumps({"cities": cities}),
            content_type="application/json",
            status=200
        )
       
