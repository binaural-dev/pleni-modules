# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    product_uom_domain = fields.Many2many(related='product_id.product_tmpl_id.product_uom_ids', readonly=True)
