===============================
Auth JWT & Custom Endpoint
===============================


A custom module for ``auth_jwt``.

**Table of contents**

.. contents::
   :local:

Usage
=====

This modules creates a JWT validator named ``api``, and adds a
``/api/auth_jwt/whoami`` route which returns information about the partner
identified in the token.

The ``whoami`` endpoint can be invoked as such, assuming `python-jose
<https://pypi.org/project/python-jose/>`_ is installed.


.. code-block:: python

    # /usr/bin/env python3
    import time

    import requests
    from jose import jwt

    token = jwt.encode(
        {
            "aud": "auth_jwt_api",
            "iss": "some issuer",
            "exp": time.time() + 60,
            "email": "mark.brown23@example.com",
        },
        key="thesecret",
        algorithm=jwt.ALGORITHMS.HS256,
    )
    r = requests.get(
        "http://localhost:8069/api/auth_jwt/whoami",
        headers={"Authorization": "Bearer " + token},
    )
    r.raise_for_status()
    print(r.json())

Endpoints:
==========

Main endpoints
~~~~~~~~~~~~~~

* [GET] /api/auth_jwt (login with JWT token)
* [GET] /api/auth_jwt/whoami (get information about the partner identified in the token)


Partners endpoints
~~~~~~~~~~~~~~~~~~

* [GET] /api/res_partner (list partners)
* [GET] /api/res_partner/{id} (get partner by id)
* [POST] /api/res_partner (create a partner)


Products endpoints
~~~~~~~~~~~~~~~~~~

* [GET] /api/product (list products)
* [GET] /api/product/{id} (get product by id)


Sales orders endpoints
~~~~~~~~~~~~~~~~~~~~~~

* [GET] /api/sale_order (list sales orders)
* [GET] /api/sale_order/{id} (get sale order by id)
* [POST] /api/sale_order (create a sale order)


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/server-auth/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/server-auth/issues/new?body=module:%20auth_jwt_demo%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* ACSONE SA/NV

Contributors
~~~~~~~~~~~~

* Stéphane Bidoul <stephane.bidoul@acsone.eu>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-sbidoul| image:: https://github.com/sbidoul.png?size=40px
    :target: https://github.com/sbidoul
    :alt: sbidoul

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-sbidoul| 

This module is part of the `OCA/server-auth <https://github.com/OCA/server-auth/tree/16.0/auth_jwt_demo>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
