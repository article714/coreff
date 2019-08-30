# -*- coding: utf-8 -*-
# @author: J. Carette
# @author: C. Guychard
# @copyright: ©2018-2019 Article 714
# @license: AGPL v3

{
    "name": u"CoreFF: CreditSafe",
    "version": u"12.0.1.0.0",
    "category": u"CoreFF",
    "author": u"Article714",
    "license": u"AGPL-3",
    "website": u"https://www.article714.org",
    "summary": "",
    "depends": ["coreff_base", "l10n_fr", "web"],
    "data": [
        "views/coreff_creditsafe_assets.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_views.xml",
        "data/cron.xml",
        "security/creditsafe_authent_security.xml",
    ],
    "qweb": [
        "static/src/xml/create_from_button.xml",
        "static/src/xml/creditsafe_autocomplete.xml",
    ],
    "installable": True,
    "images": [],
    "application": False,
}
