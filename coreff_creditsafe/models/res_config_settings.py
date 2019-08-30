# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import requests
import json
from odoo import fields, models, _, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    creditsafe_url = fields.Char()
    creditsafe_username = fields.Char()
    creditsafe_password = fields.Char()
    creditsafe_token = fields.Text()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['creditsafe_url'] = self.env['ir.config_parameter'].sudo().get_param('coreff_creditsafe.creditsafe_url', default="")
        res['creditsafe_username'] = self.env['ir.config_parameter'].sudo().get_param('coreff_creditsafe.creditsafe_username', default="")
        res['creditsafe_password'] = self.env['ir.config_parameter'].sudo().get_param('coreff_creditsafe.creditsafe_password', default="")
        res['creditsafe_token'] = self.env['ir.config_parameter'].sudo().get_param('coreff_creditsafe.creditsafe_token', default="")

        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('coreff_creditsafe.creditsafe_url', self.creditsafe_url)
        self.env['ir.config_parameter'].sudo().set_param('coreff_creditsafe.creditsafe_username', self.creditsafe_username)
        self.env['ir.config_parameter'].sudo().set_param('coreff_creditsafe.creditsafe_password', self.creditsafe_password)

        headers = {"accept": "application/json", "Content-type": "application/json"}
        data = {"username": self.creditsafe_username, "password": self.creditsafe_password}
        response = requests.post(("{}/authenticate".format(self.creditsafe_url)), data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            content = response.json()
            self.creditsafe_token = content["token"]
            self.env['ir.config_parameter'].sudo().set_param('coreff_creditsafe.creditsafe_token', self.creditsafe_token)

        super(ResConfigSettings, self).set_values()