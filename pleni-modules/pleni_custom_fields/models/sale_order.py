# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    payment_state = fields.Char(string='Estado de Pago')

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

    new_client = fields.Integer(string='¿Cliente Nuevo?', compute='_get_sale_order_count')

    def _get_sale_order_count(self, partner):
            current_parent = partner.parent_id if partner.parent_id else partner
            sale_order_count = self.env['sale.order'].search_count([('partner_id', '=', current_parent.id), ('state', 'not in', ['draft', 'cancel'])])
            # return sale_order_count
            if sale_order_count <= 4:
                return "CLIENTE NUEVO"
            else:
                return ""

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    new_client = fields.Integer(string='¿Cliente Nuevo?', compute='_get_sale_order_count')

    def _get_sale_order_count(self, partner):
            current_parent = partner.parent_id if partner.parent_id else partner
            sale_order_count = self.env['sale.order'].search_count([('partner_id', '=', current_parent.id), ('state', 'not in', ['draft', 'cancel'])])
            # return sale_order_count
            if sale_order_count <= 4:
                return "CLIENTE NUEVO"
            else:
                return ""
            
class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    new_client = fields.Integer(string='¿Cliente Nuevo?', compute='_get_sale_order_count')

    def _get_sale_order_count(self, partner):
            current_parent = partner.parent_id if partner.parent_id else partner
            sale_order_count = self.env['sale.order'].search_count([('partner_id', '=', current_parent.id), ('state', 'not in', ['draft', 'cancel'])])
            # return sale_order_count
            if sale_order_count <= 4:
                return "CLIENTE NUEVO"
            else:
                return ""
