# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class PaymentAcquirerInherit(models.Model):
    _inherit = 'payment.acquirer'

    sale_relation_view = fields.Boolean(string="Mostrado en el módulo de ventas")


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    payment_methods = fields.Many2many('payment.acquirer', string='Método de Pago')