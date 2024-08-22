"""Controller for the sale order model."""

import json
from odoo.http import Controller, Response, request, route

from .utils import clean_html


class JWTSaleOrderController(Controller):
    """Controller to handle sale order records.
    - [GET] /sale_order: get all sale order records.
    - [GET] /sale_order/<int:order_id>: get a sale order record by id.
    - [POST] /sale_order: create a sale order record.
    """

    @route(
        "/api/sale_order",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_sale_order(self):
        """Get all sale order records.
        - Return a JSON object with a list of sale order records.
        """
        data = {}
        sale_order = request.env["sale.order"].with_user(request.env.uid).search([])
        data.update(
            sale_order=[
                {
                    "name": order.name,
                    "date": str(order.date_order),
                    "id": order.id,
                    "partner_id": order.partner_id.id,
                    "amount_total": order.amount_total,
                    "state": order.state or "N/A",
                    "lines": [
                        {
                            "id": line.id,
                            "product_id": line.product_id.id,
                            "product_name": line.product_id.name,
                            "quantity": line.product_uom_qty,
                            "price": line.price_unit,
                        }
                        for line in order.order_line
                    ],
                }
                for order in sale_order
            ]
        )
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/sale_order/<int:order_id>",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_sale_order_by_id(self, order_id):
        """Get a sale order record by id.
        - Return a JSON object with the sale order record.
        - Return a JSON object with an error if the sale order record is not found.
        """
        data = {}
        sale_order = (
            request.env["sale.order"].with_user(request.env.uid).browse(order_id)
        )
        if sale_order:
            data.update(
                sale_order={
                    "name": sale_order.name,
                    "date": str(sale_order.date_order),
                    "id": sale_order.id,
                    "partner_id": sale_order.partner_id.id,
                    "amount_total": sale_order.amount_total,
                    "state": sale_order.state or "N/A",
                    "lines": [
                        {
                            "id": line.id,
                            "product_id": line.product_id.id,
                            "product_name": line.product_id.name,
                            "quantity": line.product_uom_qty,
                            "price": line.price_unit,
                        }
                        for line in sale_order.order_line
                    ],
                }
            )
        else:
            data.update({"error": "Sale order not found."})
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/sale_order",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["POST", "OPTIONS"],
    )
    def create_sale_order(self):
        """Create a sale order record.
        - Return a JSON object with the created sale order record.
        - Return a JSON object with an error if the sale order record is not created.
        """
        data = {}
        try:
            payload = json.loads(request.httprequest.data)
            sale_order = (
                request.env["sale.order"]
                .with_user(request.env.uid)
                .create(
                    {
                        "name": payload.get("name"),
                        "date_order": payload.get("date"),
                        "partner_id": payload.get("partner_id"),
                        "amount_total": payload.get("amount_total"),
                        "order_line": [
                            (
                                0,
                                0,
                                {
                                    "product_id": line.get("product_id"),
                                    "product_uom_qty": line.get("quantity"),
                                    "price_unit": line.get("price"),
                                },
                            )
                            for line in payload.get("lines")
                        ],
                    }
                )
            )
            data.update(
                sale_order={
                    "name": sale_order.name,
                    "date": str(sale_order.date_order),
                    "id": sale_order.id,
                    "partner_id": sale_order.partner_id.id,
                    "amount_total": sale_order.amount_total,
                    "state": sale_order.state or "N/A",
                    "lines": [
                        {
                            "id": line.id,
                            "product_id": line.product_id.id,
                            "product_name": line.product_id.name,
                            "quantity": line.product_uom_qty,
                            "price": line.price_unit,
                        }
                        for line in sale_order.order_line
                    ],
                }
            )
        except Exception as e:
            data.update({"error": str(e)})
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/sale_order/payment_terms",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_payment_terms(self):
        """Get all payment terms records.
        - Return a JSON object with a list of payment terms records.
        """
        data = {}
        payment_terms = (
            request.env["account.payment.term"].with_user(request.env.uid).search([])
        )
        data.update(
            payment_terms=[
                {
                    "id": term.id,
                    "name": term.name,
                    "note": clean_html(term.note) or "N/A",
                }
                for term in payment_terms
            ]
        )
        return Response(json.dumps(data), content_type="application/json", status=200)
