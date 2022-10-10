# -*- coding: utf-8 -*-
import logging
from odoo import api, models
from odoo.exceptions import UserError

ORDERS_DELIVERY_STATUS = ['draft', 'waiting', 'confirmed', 'assigned', 'done', 'cancel']

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_status(self):
        stock_picking_lines = self.env['stock.picking'].search([('origin','=',self.name)])
        lines_status = [line.state for line in stock_picking_lines]
 
        if not lines_status:
            return 'draft'
        if 'cancel' in lines_status:
            return 'cancel'
        for delivery_status in ORDERS_DELIVERY_STATUS:
            if delivery_status in lines_status:
                return delivery_status
        return ''
        