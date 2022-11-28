# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import fields, models


_logger = logging.getLogger(__name__)


class CoreffConfig(models.TransientModel):
    _inherit = "res.config.settings"

    module_coreff_creditsafe = fields.Boolean(
        string="Synchronize data with CreditSafe",
        help="""Use the Credit Safe services to update partner data""",
    )

    module_coreff_societecom = fields.Boolean(
        string="Synchronize data with Societe.com",
        help="Use the Societe.com services to update partner data",
    )

    module_coreff_informa = fields.Boolean(
        string="Synchronize data with Informa",
        help="Use the Informa services to update partner data",
    )
