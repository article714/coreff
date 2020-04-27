# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models
from odoo.addons.coreff_creditsafe.mixins.creditsafe_data_mixin import (
    CreditSafeDataMixin,
)


class Partner(CreditSafeDataMixin, models.Model):
    """
    Add creditsafe fields from CreditSafeDataMixin
    """

    _inherit = "res.partner"
