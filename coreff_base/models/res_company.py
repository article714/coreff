# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    coreff_connector_id = fields.Many2one("coreff.connector")
    coreff_company_code_mandatory = fields.Boolean()