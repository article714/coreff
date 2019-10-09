# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api
from odoo.tools.safe_eval import safe_eval


class CoreffAPI(models.Model):
    """
    Coreff API
    """

    _name = "coreff.api"

    @api.model
    def get_companies(self, arguments):
        """
        Get companies
        """
        company = self.env.user.company_id
        connector = company.coreff_connector_id
        if connector:
            return safe_eval(
                connector.get_companies_def,
                {"self": connector, "arguments": arguments},
            )

    @api.model
    def get_company(self, arguments):
        """
        Get company information
        """
        company = self.env.user.company_id
        connector = company.coreff_connector_id
        if connector:
            return safe_eval(
                connector.get_company_def,
                {"self": connector, "arguments": arguments},
            )
