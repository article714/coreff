# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class CoreffCredentials(models.Model):
    """
    Credentials management
    """

    _name = "coreff.credentials"
    _description = "Coreff API Credientials"
    _order = "create_date DESC"

    url = fields.Char()

    username = fields.Char()

    token = fields.Text()

    @api.model
    def update_token(self, url, username, token):
        credentials = self.get_credentials(url, username)
        if credentials:
            credentials.write({"token": token})
        else:
            values = {}
            values["url"] = url
            values["username"] = username
            values["token"] = token
            self.env["coreff.credentials"].create(values)

    @api.model
    def get_credentials(self, url, username):
        credentials = self.env["coreff.credentials"].search(
            [("url", "=", url), ("username", "=", username)]
        )

        res = credentials
        flag = False
        for rec in credentials:
            if not flag:
                res = rec
                flag = True
            else:
                rec.unlink()

        return res
