# -*- coding: utf-8 -*-
# @author: J. Carette
# @author: C. Guychard
# @copyright: ©2018-2019 Article 714
# @license: LGPL v3

{
    "name": "CoreFF: Societe.com",
    "version": "12.0.1.0.0",
    "category": "CoreFF",
    "author": "Article714",
    "license": "LGPL-3",
    "website": "https://www.article714.org",
    "description": """
CoreFF - CreditSafe
===================

The aim of this module is to get financial informations
from Societe.com and add them to res_partner model.

Of course, you need a Societe.com account and set its properties
into "financial informations" configuration menu.

**Credits:** .
""",
    "depends": ["coreff_base"],
    "data": ["views/coreff_config_view.xml"],
    "qweb": ["static/src/xml/create_from_button.xml"],
    "installable": True,
    "images": [],
    "application": False,
}
