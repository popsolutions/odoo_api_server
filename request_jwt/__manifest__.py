# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Request endpoints with JWT",
    "summary": """
        Custom module for auth_jwt and custom endpoints.
    """,
    "version": "16.0.1.1.1",
    "license": "LGPL-3",
    "category": "Applications",
    "author": "PopSolutions <pop.coop>",
    "maintainers": ["sbidoul"],
    "website": "https://github.com/popsolutions/odoo_api_server",
    "depends": ["auth_jwt"],
    "images": ["static/description/icon.png"],
    "data": ["data/auth_jwt_validator.xml"],
    "demo": ["demo/auth_jwt_validator.xml"],
}
