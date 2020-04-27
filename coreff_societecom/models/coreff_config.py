# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models, _


class CoreffConfig(models.TransientModel):
    _inherit = "res.config.settings"

    societeComUrl = fields.Char(
        string=_(u"URL"), help=_(u"URL d'accès au service Societe.com.")
    )

    societeComLogin = fields.Char(
        string=_(u"Identifiant"),
        help=_(u"Login d'accès au service Societe.com."),
    )

    societeComPassword = fields.Char(
        string=_(u"Mot de passe"),
        help=_(u"Mot de passe d'accès au service Societe.com."),
    )
