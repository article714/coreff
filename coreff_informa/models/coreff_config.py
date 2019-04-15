# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models, _

class CoreffConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    informaUrl = fields.Char(string=_(u'URL'),
                                help=_(u'URL d\'accès au service Informa.'))
                                
    informaLogin = fields.Char(string=_(u'Identifiant'),
                                help=_(u'Login d\'accès au service Informa.'))
    
    informaPassword = fields.Char(string=_(u'Mot de passe'),
                                help=_(u'Mot de passe d\'accès au service Informa.'))                                