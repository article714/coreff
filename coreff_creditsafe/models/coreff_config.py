# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models, _

class CoreffConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    creditSafeUrl = fields.Char(string=_(u'WSDL'),
                                help=_(u'URL d\'accès au service GetData de CreditSafe.'))
                                
    creditSafeLogin = fields.Char(string=_(u'Identifiant'),
                                help=_(u'Login d\'accès au service GetData de CreditSafe.'))
    
    creditSafePassword = fields.Char(string=_(u'Mot de passe'),
                                help=_(u'Mot de passe d\'accès au service GetData de CreditSafe.'))                                