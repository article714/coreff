# ©2018-2019 Article714
# # License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class CoreffConnector(models.Model):
    """
    Connector with API
    """

    _name = "coreff.connector"
    _description = "Coreff API Connector"

    name = fields.Char(required=True)

    autocomplete_fields = fields.Char()

    get_companies_def = fields.Char(required=True)

    get_company_def = fields.Char(required=True)
