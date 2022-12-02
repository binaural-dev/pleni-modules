# -*- coding: utf-8 -*-

from odoo import models, fields, api
from asyncio.log import logger
from odoo.exceptions import UserError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    amount_untaxed_without_delivery = fields.Float('Subtotal', compute='_compute_amount_untaxed_without_delivery')

    def _compute_amount_untaxed_without_delivery(self):
        for order in self:
            subtotal = 0
            for line in order.order_line:
                if not line.is_delivery:
                    subtotal += line.price_subtotal

            self.amount_untaxed_without_delivery = subtotal


