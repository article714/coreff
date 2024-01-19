# @author: J. Carette
# @author: C. Guychard
# @author: Chris Mann (Open User Systems)
# @copyright: ©2018-2019 Article 714
# @license: LGPL v3

{
    "name": "CoreFF: Basic Module",
    "version": "16.0.1.0.1",
    "category": "CoreFF",
    "author": "Article714",
    "license": "LGPL-3",
    "website": "https://www.article714.org",
    "summary": "Manage Core Financial Data: base module",
    "depends": ["base"],
    "data": [
        "security/coreff_security.xml",
        "views/coreff_config_views.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
    "images": [],
    "application": False,
    "assets": {
        "web.assets_backend": [
            "coreff_base/static/src/scss/*",
            "coreff_base/static/src/js/*",
            "coreff_base/static/src/xml/*",
            "coreff_base/static/src/coreff_autocomplete/*",
        ],
    },
}
