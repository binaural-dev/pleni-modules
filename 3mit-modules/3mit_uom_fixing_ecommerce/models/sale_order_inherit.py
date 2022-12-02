# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_uom_domain = fields.Many2many(related='product_template_id.product_uom_ids', readonly=True)
