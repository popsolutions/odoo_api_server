"""Controller to handle product records."""

import json

from odoo.http import Controller, Response, request, route


class JWTProductsController(Controller):
    """Controller to handle product records."""

    @route(
        "/api/product",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_products(self):
        """Get all product records.
        - Return a JSON object with a list of product records.
        """
        data = {}
        products = request.env["product.product"].with_user(request.env.uid).search([])
        data.update(
            products=[
                {
                    "name": product.name,
                    "price": product.list_price,
                    "id": product.id,
                    "description": product.description_sale or "N/A",
                }
                for product in products
            ]
        )
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/product/<int:product_id>",
        type="http",
        auth="jwt_api",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_product_by_id(self, product_id):
        """Get a product record by id.
        - Return a JSON object with the product record.
        - Return a JSON object with an error if the product record is not found.
        """
        data = {}
        product = (
            request.env["product.product"].with_user(request.env.uid).browse(product_id)
        )
        if product:
            data.update(
                product={
                    "name": product.name,
                    "price": product.list_price,
                    "id": product.id,
                    "description": product.description_sale or "N/A",
                }
            )
            return Response(
                json.dumps(data), content_type="application/json", status=200
            )
        return Response(
            json.dumps({"error": "Product not found."}),
            content_type="application/json",
            status=404,
        )
