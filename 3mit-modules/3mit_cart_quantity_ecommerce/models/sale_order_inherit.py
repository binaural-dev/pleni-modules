# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.product_uom_qty', 'order_line.product_id')
    def _compute_cart_info(self):
        for order in self:
            order.cart_quantity = len([line for line in order.order_line if not line.is_delivery])
            # order.cart_quantity = int(sum(order.mapped('website_order_line.product_uom_qty')))
            order.only_services = all(line.product_id.type in ('service', 'digital') for line in order.website_order_line)
