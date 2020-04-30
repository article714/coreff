# -*- coding: utf-8 -*-
"""
Created on 8 August 2018

@author: J. Carette
@copyright: ©2018-2019 Article 714
@license: LGPL v3
"""

import logging

from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    coreff_search_is_head_office = fields.Boolean(
        default=True, string="Head offices only", store=False
    )

    # -------------------------
    # unimplemented method that will be defined in other module to update from HMI
    # only runs validators by default
    def interactive_update(self):
        # just call data valition methods
        self.run_validators()
        return

    # -------------------------
    # method to validate values from CoreFF Partner model
    def run_validators(self):
        # TODO
        return

    @api.one
    def create_from(self):
        # TODO
        logging.debug("CREATE FROM CALL")
        return
