# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CoreffCredentials(models.Model):
    """
    Credentials management
    """

    _name = "coreff.credentials"

    url = fields.Char()

    username = fields.Char()

    token = fields.Text()

    @api.model
    def update_token(self, url, username, token):
        credentials = self.get_token(url, username)
        if credentials:
            credentials.write({"token": token})
        else:
            values = {}
            values["url"] = url
            values["username"] = username
            values["token"] = token
            self.env["coreff.credentials"].create(values)

    @api.model
    def get_token(self, url, username):
        return self.env["coreff.credentials"].search(
            [("url", "=", url), ("username", "=", username)]
        )
