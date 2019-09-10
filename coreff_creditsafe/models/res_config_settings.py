# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import json
import requests
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """
    Ajout des settings pour l'accès à l'API CreditSafe
    """

    _inherit = "res.config.settings"

    creditsafe_url = fields.Char()
    creditsafe_username = fields.Char()
    creditsafe_password = fields.Char()
    creditsafe_token = fields.Text()

    @api.model
    def get_values(self):
        """
        GetValues
        """
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        res["creditsafe_url"] = params.get_param(
            "coreff_creditsafe.creditsafe_url", default=""
        )
        res["creditsafe_username"] = params.get_param(
            "coreff_creditsafe.creditsafe_username", default=""
        )
        res["creditsafe_password"] = params.get_param(
            "coreff_creditsafe.creditsafe_password", default=""
        )
        res["creditsafe_token"] = params.get_param(
            "coreff_creditsafe.creditsafe_token", default=""
        )

        return res

    @api.model
    def set_values(self):
        """
        SetValues
        """
        params = self.env["ir.config_parameter"].sudo()
        params.set_param(
            "coreff_creditsafe.creditsafe_url", self.creditsafe_url
        )
        params.set_param(
            "coreff_creditsafe.creditsafe_username", self.creditsafe_username
        )
        params.set_param(
            "coreff_creditsafe.creditsafe_password", self.creditsafe_password
        )

        headers = {
            "accept": "application/json",
            "Content-type": "application/json",
        }
        data = {
            "username": self.creditsafe_username,
            "password": self.creditsafe_password,
        }
        response = requests.post(
            ("{}/authenticate".format(self.creditsafe_url)),
            data=json.dumps(data),
            headers=headers,
        )
        if response.status_code == 200:
            content = response.json()
            self.creditsafe_token = content["token"]
            params.set_param(
                "coreff_creditsafe.creditsafe_token", self.creditsafe_token
            )

        super(ResConfigSettings, self).set_values()
