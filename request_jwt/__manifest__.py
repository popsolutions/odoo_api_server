# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Auth JWT & Custom Endpoints",
    "summary": """
        Custom module for auth_jwt and custom endpoints.""",
    "version": "16.0.1.1.1",
    "license": "LGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "maintainers": ["sbidoul"],
    "website": "https://github.com/OCA/server-auth",
    "depends": ["auth_jwt"],
    "data": ["data/auth_jwt_validator.xml"],
    "demo": ["demo/auth_jwt_validator.xml"],
}
