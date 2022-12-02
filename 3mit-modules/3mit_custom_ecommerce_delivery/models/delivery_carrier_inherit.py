# -*- coding: utf-8 -*-
import logging
from odoo import api, models
from odoo.exceptions import UserError


class DeliveryCarrierInherit(models.Model):
    _inherit = 'delivery.carrier'

    def rate_shipment(self, order):
        res = super(DeliveryCarrierInherit, self).rate_shipment(order)
        if order.amount_untaxed - self.fixed_price < self.amount:
            res['price'] = self.fixed_price
        else:
            res['price'] = 0
        return res
        