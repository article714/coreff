# coding: utf-8

# @author: J. Carette
# @author: C. Guychard
# @copyright: ©2018-2019 Article 714
# @license: LGPL v3

{
    "name": "CoreFF: Basic Module",
    "version": "12.0.1.0.0",
    "category": "CoreFF",
    "author": "Article714",
    "license": "LGPL-3",
    "website": "https://www.article714.org",
    "summary": "Manage Core Financial Data: base module",
    "depends": ["base"],
    "data": [
        "security/coreff_security.xml",
        "views/coreff_autocomplete_assets.xml",
        "views/coreff_config_views.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
    ],
    "qweb": ["static/src/xml/coreff_autocomplete.xml"],
    "installable": True,
    "images": [],
    "application": False,
}
