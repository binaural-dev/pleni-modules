# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.depends('partner_id')
    @api.onchange('partner_id')
    def search_exists_so_with_partner(self):
        for rec in self:
            rec.is_new_client = True
            domain = [('partner_id', '=', rec.partner_id.id)]
            if len(rec.ids) > 0:
                domain.append(('id', 'not in', rec.ids))
            sale_order_exists = self.env['sale.order'].search(domain)
            if sale_order_exists:
                rec.is_new_client = False

    is_new_client = fields.Boolean('¿Primera orden?', compute='search_exists_so_with_partner', store=True)
