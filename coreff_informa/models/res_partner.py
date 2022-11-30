# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models
from ..mixins.informa_data_mixin import (
    InformaDataMixin,
)


class Partner(InformaDataMixin, models.Model):
    """
    Add informa fields from InformaDataMixin
    """

    _inherit = "res.partner"
