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
        "security/creditsafe_security.xml",
        "views/res_company_views.xml",
        "views/res_partner_views.xml",
        "data/coreff_connector.xml",
        "data/cron.xml",
    ],
    "qweb": [],
    "installable": True,
    "images": [],
    "application": False,
}
