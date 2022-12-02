# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import _, api, models, fields
from odoo.osv import expression


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('commercial_name', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
