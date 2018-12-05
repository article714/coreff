# -*- coding: utf-8 -*-
'''
Created on 2018, Sept 1

@author: J. Carette
@copyright: ©2018 Article 714
@license: AGPL v3
'''

import logging

from odoo import exceptions, api, fields, models, _


class CreateFromModel(models.TransientModel):
    _name = 'coreff_creditsafe_createfrom_wizard'
    _description = u"Create a res_partner with siret (siren + nic)"

    siren = fields.Char(
        string='SIREN', size=9,
        help="The SIREN number is the official identity "
        "number of the company in France. It makes "
        "the first 9 digits of the SIRET number.")
    
    nic = fields.Char(
        string='NIC', size=5,
        help="The NIC number is the official rank number "
        "of this office in the company in France. It "
        "makes the last 5 digits of the SIRET "
        "number.")
    
    siret = fields.Char(
        compute='_compute_siret', string='SIRET', size=14, store=True,
        help="The SIRET number is the official identity number of this "
        "company's office in France. It is composed of the 9 digits "
        "of the SIREN number and the 5 digits of the NIC number, ie. "
        "14 digits.")


    @api.multi
    @api.depends('siren', 'nic')
    def _compute_siret(self):
        """Concatenate the SIREN and NIC to form the SIRET"""
        for rec in self:
            if rec.siren:
                if rec.nic:
                    rec.siret = rec.siren + rec.nic
                else:
                    rec.siret = rec.siren + '*****'
            else:
                rec.siret = ''


    def open_view(self):
        self.ensure_one
        action = self.env.ref('dynalec_purchase.view_cutoff_purchase_action').read()[0]
        computed_domain = []

        computed_domain.append(('state', 'in', ('done', 'purchase')))

        if self.date:
            computed_domain.append(('date_order', '<', self.date))

        computed_domain.append('|')
        computed_domain.append(('qty_to_receive', '>', 0))
        computed_domain.append(('qty_to_invoice', '>', 0))

        action.update({
            'domain': computed_domain
        })

        return action
                                