# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CoreffConnector(models.Model):
    """
    Connector with API
    """

    _name = "coreff.connector"
    _description = "Coreff API Connector"

    name = fields.Char(required=True)

    get_companies_def = fields.Char(required=True)

    get_company_def = fields.Char(required=True)
