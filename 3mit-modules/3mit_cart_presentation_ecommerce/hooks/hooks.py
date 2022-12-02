# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def get_most_sold_products(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sale_order_lines = env['sale.order.line'].search([('state', '=', 'sale')])
    for line in sale_order_lines:
        line.product_template_id.times_sold += line.product_uom_qty
