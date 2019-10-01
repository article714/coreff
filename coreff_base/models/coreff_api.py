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
    def authenticate(self):
        """
        Authent
        """
        company = self.env.user.company_id
        connector = company.coreff_connector_id
        if connector:
            return safe_eval(connector.authenticate_def, {"self": connector})

    @api.model
    def get_companies(self, countries, language, is_siret, value):
        """
        Get companies
        """
        company = self.env.user.company_id
        connector = company.coreff_connector_id
        if connector:
            return safe_eval(
                connector.get_companies_def,
                {
                    "self": connector,
                    "countries": countries,
                    "language": language,
                    "is_siret": is_siret,
                    "value": value,
                },
            )

    @api.model
    def get_company(self, company_id):
        """
        Get company information
        """
        company = self.env.user.company_id
        connector = company.coreff_connector_id
        if connector:
            return safe_eval(
                connector.get_company_def,
                {"self": connector, "company_id": company_id},
            )
