# -*- coding: utf-8 -*-
'''
Created on 8 August 2018

@author: J. Carette
@copyright: ©2018 Article 714
@license: AGPL v3
'''

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)

class CoreffPartner(models.Model):
    _inherit = 'res.partner'

    company_number = fields.Char(string=_(u'SIRET'), index=True)
    siren = fields.Char(string=_(u'SIRET'), index=True)
    nic = fields.Char(string=_(u'NIC'))
    
    #-------------------------
    # unimplemented method that will be defined in other module to update from HMI
    # only runs validators by default
    def interactive_update(self):
        #just call data valition methods 
        self.run_validators()
        return
    
    #-------------------------
    # method to validate values from CoreFF Partner model
    def run_validators(self):
        #TODO
        return

