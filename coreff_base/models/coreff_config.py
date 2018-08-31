# -*- coding: utf-8 -*-
# ©2018 Article714
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from __builtin__ import str
import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)

PARAMS = [
    ("creditSafeUrl", "coreff.creditSafeUrl"),
    ("creditSafeLogin", "coreff.creditSafeLogin"),
    ("creditSafePassword", "coreff.creditSafePassword"),
    ("societeComUrl", "coreff.SocieteComUrl"),
    ("societeComLogin", "coreff.SocieteComLogin"),
    ("societeComPassword", "coreff.SocieteComPassword")
]


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
            
            _logger.info("GE_ATTR = "+str(getattr(self, field_name, ''))+" TYPE = "+str(type(getattr(self, field_name, '')))+" ")    
            if isinstance(self[field_name], models.Model):
                if param_value != None and param_value != '':
                    val = self[field_name].search([('id', '=', param_value)])
                    res[field_name] = val.id
            elif isinstance(self[field_name], str):
                res[field_name] = param_value.strip()
            elif isinstance(self[field_name], unicode):
                res[field_name] = param_value.strip()
            elif isinstance(self[field_name], bool):
                res[field_name] = True if param_value == '1' else False
            
            
        return res
