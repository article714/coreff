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
    ("societeComPassword", "coreff.SocieteComPassword"),
    ("coucou", "coreff.coucou")
]


class CoreffConfig(models.TransientModel):
    _name = 'coreff.config.settings'
    _inherit = 'res.config.settings'

    coucou = fields.Many2one(comodel_name='res.partner')
    coincoin = fields.Boolean()

    @api.one
    def set_params(self):
        for field_name, key_name in PARAMS:
            obj = getattr(self, field_name, '')
            value = None

            all_fields = self.fields_get()

            if field_name in all_fields:
                field = all_fields[field_name]
                field_type = field['type']

                if field_type == 'many2one':
                    value = obj.id
                elif field_type == 'char':
                    value = obj.strip()
                elif isinstance(obj, 'boolean'):
                    value = '1' if obj else '0'

                self.env['ir.config_parameter'].set_param(key_name, value)

    def get_default_params(self, context=None):
        res = {}

        all_fields = self.fields_get()

        for field_name, key_name in PARAMS:
            param_value = self.env['ir.config_parameter'].get_param(key_name, '')
            if field_name in all_fields:

                field = all_fields[field_name]
                field_type = field['type']

                if field_type == 'many2one':
                    if param_value != None and param_value != '':
                        val = self[field_name].search([('id', '=', param_value)])
                        res[field_name] = val.id
                elif field_type == 'char':
                    res[field_name] = param_value.strip()
                elif field_type == 'boolean':
                    res[field_name] = (param_value == '1')
                elif field_type == 'integer':
                    res[field_name] = int(param_value)
                elif field_type == 'datetime':
                    res[field_name] = param_value
            else:
                _logger.warning("GE_ATTR = " + str(getattr(self, field_name, '')) +
                                " TYPE = " + str(type(getattr(self, field_name, ''))) + " ")

        return res
