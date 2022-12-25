# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

ORDERS_DELIVERY_STATUS = ['draft', 'waiting', 'confirmed', 'assigned', 'done', 'cancel']


class PaymentAcquirerInherit(models.Model):
    _inherit = 'payment.acquirer'

    sale_relation_view = fields.Boolean(string="Mostrado en el módulo de ventas")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    payment_methods = fields.Many2many('payment.acquirer', string='Método de Pago')

    def _get_delivery_status(self):
        stock_picking_lines = self.env['stock.picking'].search([('origin','=',self.name)])
        lines_status = [line.state for line in stock_picking_lines]
 
        if not lines_status:
            return 'draft'
        if len(lines_status) > 1:
            if lines_status[0] == 'cancel':
                return 'cancel'
        else:
            if 'cancel' in lines_status:
                return 'cancel'
        for delivery_status in ORDERS_DELIVERY_STATUS:
            if delivery_status in lines_status:
                return delivery_status
        return ''

    def _get_order_fails(self):
        to_invoice = False
        not_delivered = []
        pickings = self.env['sale.order.line'].search([('order_id', '=', self.id)])

        for p in pickings:
            if (p.invoice_status == 'to invoice' or  p.invoice_status == 'invoiced') and p.state == 'sale' and not p.is_delivery and "descuento" not in p.name.lower():
                to_invoice = True
            if p.product_uom_qty > p.qty_to_invoice:
                not_delivered.append(p)
        
     
        return True if to_invoice and not_delivered else False