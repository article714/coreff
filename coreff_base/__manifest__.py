# @author: J. Carette
# @author: C. Guychard
# @author: Chris Mann (Open User Systems)
# @copyright: ©2018-2019 Article 714
# @license: LGPL v3

{
    "name": u"CoreFF: Basic Module",
    "version": u"15.0.1.0.0",
    "category": u"CoreFF",
    "author": u"Article714",
    "license": u"LGPL-3",
    "website": u"https://www.article714.org",
    "summary": u"Manage Core Financial Data: base module",
    "depends": ["base"],
    "data": [
        "security/coreff_security.xml",
        "views/coreff_config_views.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
    ],
    "qweb": ["static/src/xml/coreff_autocomplete.xml"],
    "installable": True,
    "images": [],
    "application": False,
    "assets": {
        "web.assets_backend": [
            "coreff_base/static/src/scss/coreff_autocomplete.scss",
            "coreff_base/static/src/js/create_from_button.js",
            "coreff_base/static/src/js/coreff_autocomplete_core.js",
            "coreff_base/static/src/js/coreff_autocomplete_fieldchar.js",
        ]
    }
}
