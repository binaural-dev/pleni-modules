# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    is_new_client = fields.Boolean(string='¿Cliente Nuevo?', compute='search_exists_so_with_partner', store=True)

    @api.depends('partner_id')
    def search_exists_so_with_partner(self):
        for record in self:
            if record.partner_id:
                so_count = self.env['sale.order'].search_count([('partner_id', '=', record.partner_id.id), ('state', 'not in', ['draft', 'cancel'])])
                if so_count > 4:
                    record.is_new_client = False
                else:
                    record.is_new_client = True
            else:
                record.is_new_client = False