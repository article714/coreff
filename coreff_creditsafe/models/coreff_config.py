# -*- coding: utf-8 -*-
# ©2018 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from __builtin__ import str

from odoo import fields, models, _

class CoreffConfig(models.TransientModel):
    _inherit = 'coreff.config.settings'

    CreditSafeUrl = fields.Char(string=_(u'URL'),
                                help=_(u'URL d\'accès au service GetData de CreditSafe.'))
                                
    CreditSafeLogin = fields.Char(string=_(u'Identifiant'),
                                help=_(u'Login d\'accès au service GetData de CreditSafe.'))
    
    CreditSafePassword = fields.Char(string=_(u'Mot de passe'),
                                help=_(u'Mot de passe d\'accès au service GetData de CreditSafe.'))                                