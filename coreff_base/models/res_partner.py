# -*- coding: utf-8 -*-
"""
Created on 8 August 2018

@author: J. Carette
@copyright: ©2018-2019 Article 714
@license: LGPL v3
"""

import logging

from odoo import api, models, fields
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"

    _sql_constraints = [
        (
            "coreff_company_code_uniq",
            "unique (coreff_company_code, company_id)",
            "Company code must be unique",
        )
    ]

    coreff_company_code = fields.Char()

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

    @api.multi
    def write(self, values):
        """
        Set is_head_office always True for next edition
        """
        res = super(ResPartner, self).write(values)
        return res

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = (
                f"{rec.name} : {rec.coreff_company_code}"
                if rec.coreff_company_code
                else rec.name
            )
            res.append(name)
        return res

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if name:
            args = expression.AND(
                [
                    expression.OR(
                        [
                            [("name", operator, name)],
                            [("coreff_company_code", operator, name)],
                        ]
                    ),
                    args,
                ]
            )
        return self.search(args, limit=limit).name_get()