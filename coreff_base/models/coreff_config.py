# -*- coding: utf-8 -*-
# ©2018 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)

PARAMS = [
    ("creditSafeUrl", "coreff.creditSafeUrl"),
    ("creditSafeLogin", "coreff.creditSafeLogin"),
    ("creditSafePassword", "coreff.creditSafePassword"),
    ("societeComUrl", "coreff.SocieteComUrl"),
    ("societeComLogin", "coreff.SocieteComLogin"),
    ("societeComPassword", "coreff.SocieteComPassword"),
    ("informaUrl", "coreff.InformaUrl"),
    ("informaLogin", "coreff.InformaLogin"),
    ("informaPassword", "coreff.InformaPassword")
]


class CoreffConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    module_coreff_creditsafe = fields.Boolean(string=u"Synchronize data with CreditSafe",
                                              help=u'Use the Credit Safe services to update partner data')

    module_coreff_societecom = fields.Boolean(string=u"Synchronize data with Societe.com",
                                              help=u'Use the Societe.com services to update partner data')
