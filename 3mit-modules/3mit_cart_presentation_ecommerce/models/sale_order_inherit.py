# -*- coding: utf-8 -*-
from odoo import models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        if self.state in ['sale', 'done']:
            for line in self.order_line:
                line.product_template_id.times_sold += line.product_uom_qty
        return res
