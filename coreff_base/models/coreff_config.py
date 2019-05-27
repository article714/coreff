# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import fields, models


_logger = logging.getLogger(__name__)


class CoreffConfig(models.TransientModel):
    _inherit = "res.config.settings"

    module_coreff_creditsafe = fields.Boolean(
        string=u"Synchronize data with CreditSafe",
        help=u"""Use the Credit Safe services to update partner data""",
    )

    module_coreff_societecom = fields.Boolean(
        string=u"Synchronize data with Societe.com",
        help=u"Use the Societe.com services to update partner data",
    )

    module_coreff_informa = fields.Boolean(
        string=u"Synchronize data with Informa",
        help=u"Use the Informa services to update partner data",
    )
