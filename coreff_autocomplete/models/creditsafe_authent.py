# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import requests
from odoo import api, models

LOGGER = logging.getLogger(__name__)


class CreditSafeAuthent(models.Model):
    """
    Authent management for CreditSafe service
    """

    _name = "creditsafe.authent"
    _description = "CreditSafe Authent"

    @api.model
    def authenticate(self):
        """
        Auto authent to access CreditSafe
        """

        params = self.env["ir.config_parameter"].sudo()
        username = params.get_param("coreff_autocomplete.username")
        password = params.get_param("coreff_autocomplete.password")
        url = params.get_param("coreff_autocomplete.url")

        data = {"username": username, "password": password}

        response = requests.post(("%s/v1/authenticate", url), data=data).json()

        if response["code"] == 200:
            LOGGER.info("Token: %s", response["token"])
            params.set_param("coreff_autocomplete.token", response["token"])
        else:
            raise Exception(response)
