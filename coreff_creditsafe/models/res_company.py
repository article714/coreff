# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    creditsafe_use_parent_company = fields.Boolean(default=False)

    creditsafe_url = fields.Char()
    creditsafe_username = fields.Char()
    creditsafe_password = fields.Char()

    creditsafe_parent_url = fields.Char(compute="_compute_parent_url")
    creditsafe_parent_username = fields.Char(
        compute="_compute_parent_username"
    )
    creditsafe_parent_password = fields.Char(
        compute="_compute_parent_password"
    )

    @api.depends("parent_id")
    @api.onchange("parent_id")
    def _compute_parent_url(self):
        for rec in self:
            if rec.parent_id and rec.creditsafe_use_parent_company:
                rec.creditsafe_parent_url = rec.get_parent_field(
                    "creditsafe_url"
                )

    @api.depends("parent_id")
    @api.onchange("parent_id")
    def _compute_parent_username(self):
        for rec in self:
            if rec.parent_id and rec.creditsafe_use_parent_company:
                rec.creditsafe_parent_username = rec.get_parent_field(
                    "creditsafe_username"
                )

    @api.depends("parent_id")
    @api.onchange("parent_id")
    def _compute_parent_password(self):
        for rec in self:
            if rec.parent_id and rec.creditsafe_use_parent_company:
                rec.creditsafe_parent_password = rec.get_parent_field(
                    "creditsafe_password"
                )

    def get_parent_field(self, field):
        for rec in self:
            if not rec.creditsafe_use_parent_company:
                return rec[field]
            elif rec.parent_id:
                return rec.parent_id.get_parent_field(field)
            else:
                return None
