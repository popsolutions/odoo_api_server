"""Controller to handle product records."""

import json


from odoo.http import Controller, Response, request, route
from .utils import get_image_from_base64, get_image_format


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
                    "id": product.id,
                    "name": product.name,
                    "price": product.list_price,
                    "description": product.description_sale or "N/A",
                    "category": {
                        "name": product.categ_id.name,
                        "id": product.categ_id.id,
                    },
                    "image": f"/api/product/{product.id}/image",
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
                    "category": {
                        "name": product.categ_id.name,
                        "id": product.categ_id.id,
                    },
                    "image": f"/api/product/{product.id}/image",
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

    @route("/api/product/categories", type="http", auth="jwt_api", csrf=False, cors="*")
    def get_product_categories(self):
        """Get all product categories.
        - Return a JSON object with a list of product categories.
        """
        data = {}
        categories = (
            request.env["product.category"].with_user(request.env.uid).search([])
        )
        data.update(
            categories=[
                {
                    "name": category.name,
                    "id": category.id,
                }
                for category in categories
            ]
        )
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route(
        "/api/product/<int:product_id>/image",
        type="http",
        auth="public",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET", "OPTIONS"],
    )
    def get_product_image_by_id(self, product_id):
        """Get a product image by id.
        - Return the product image as a binary image.
        - Return a JSON object with an error if the product image is not found.
        """
        product = request.env["product.product"].sudo().browse(product_id)
        if product:
            image = product.image_1920
            if image:
                image_format = get_image_format(image)
                image_decode = get_image_from_base64(image)
                return Response(
                    image_decode,
                    content_type=image_format,
                    status=200,
                )
        return Response(
            json.dumps({"error": "Product image not found."}),
            content_type="application/json",
            status=404,
        )
