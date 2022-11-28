# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models, _


class CoreffConfig(models.TransientModel):
    _inherit = "res.config.settings"

    societeComUrl = fields.Char(
        string="URL", help="URL d'accès au service Societe.com."
    )

    societeComLogin = fields.Char(
        string="Identifiant",
        help="Login d'accès au service Societe.com.",
    )

    societeComPassword = fields.Char(
        string="Mot de passe",
        help="Mot de passe d'accès au service Societe.com.",
    )
