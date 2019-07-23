# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
    CrefitSafe config
    """

    _inherit = "res.config.settings"

    creditsafe_url = fields.Char()
    creditsafe_username = fields.Char()
    creditsafe_password = fields.Char()
    creditsafe_token = fields.Char()
