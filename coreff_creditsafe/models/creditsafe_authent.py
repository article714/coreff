# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import requests
import json
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
        username = params.get_param("coreff_creditsafe.creditsafe_username")
        password = params.get_param("coreff_creditsafe.creditsafe_password")
        url = params.get_param("coreff_creditsafe.creditsafe_url")

        headers = {"accept": "application/json", "Content-type": "application/json"}
        data = {"username": username, "password": password}

        response = requests.post(("{}/authenticate".format(url)), data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            content = response.json()
            params.set_param("coreff_creditsafe.creditsafe_token", content["token"])
        else:
            raise Exception(response)
