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
from odoo.exceptions import UserError


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
    coreff_company_code_mandatory = fields.Boolean(
        related="company_id.coreff_company_code_mandatory"
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

    @api.model
    def create(self, values):
        res = super(ResPartner, self).create(values)
        if (
            res.is_company
            and res.coreff_company_code_mandatory
            and not res.coreff_company_code
        ):
            raise UserError("Company code is required")
        return res

    @api.multi
    def write(self, values):
        res = super(ResPartner, self).write(values)
        if (
            self.is_company
            and self.coreff_company_code_mandatory
            and not self.coreff_company_code
        ):
            raise UserError("Company code is required")
        return res

    @api.depends(
        "is_company",
        "name",
        "parent_id.name",
        "type",
        "company_name",
    )
    def _compute_display_name(self):
        diff = dict(
            show_address=None,
            show_address_only=None,
            show_email=None,
            html_format=None,
        )
        names = dict(super(ResPartner, self.with_context(**diff)).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            name = rec._get_name()
            if rec.coreff_company_code:
                name += f" : {rec.coreff_company_code}"
            res.append((rec.id, name))
        return res

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        res1 = super(ResPartner, self)._name_search(
            name, args, operator, limit, name_get_uid
        )

        res2 = self.search(
            [("coreff_company_code", operator, name)], limit=limit
        ).name_get()

        res = res1 + [v for v in res2 if v not in res1]
        return res
