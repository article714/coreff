# -*- coding: utf-8 -*-
# ©2018 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from __builtin__ import str

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

PARAMS = [
    ("CreditSafeUrl", "coreff.creditSafeUrl"),
    ("CreditSafeLogin", "coreff.creditSafeLogin"),
    ("CreditSafePassword", "coreff.creditSafePassword"),
    ("SocieteComUrl", "coreff.SocieteComUrl"),
    ("SocieteComLogin", "coreff.SocieteComLogin"),
    ("SocieteComPassword", "coreff.SocieteComPassword")]


class CoreffConfig(models.TransientModel):
    _name = 'coreff.config.settings'
    _inherit = 'res.config.settings'

    @api.one
    def set_params(self):
        for field_name, key_name in PARAMS:
            obj = getattr(self, field_name, '')
            value = None
                
            if isinstance(self[field_name], models.Model):
                value = obj.id
            elif isinstance(obj, str):
                value = obj.strip()
            elif isinstance(obj, unicode):
                value = obj.strip()
            elif isinstance(obj, bool):
                value = '1' if obj else '0'
            
            self.env['ir.config_parameter'].set_param(key_name, value)

    def get_default_params(self, context=None):
        res = {}
        for field_name, key_name in PARAMS:
            param_value = self.env['ir.config_parameter'].get_param(key_name, '')
                
            if isinstance(self[field_name], models.Model):
                if param_value != None and param_value != '':
                    val = self[field_name].search([('id', '=', param_value)])
                    res[field_name] = val.id
            elif isinstance(self[field_name], bool):
                res[field_name] = True if param_value == '1' else False
            else:
                res[field_name] = param_value.strip()
            
        return res
