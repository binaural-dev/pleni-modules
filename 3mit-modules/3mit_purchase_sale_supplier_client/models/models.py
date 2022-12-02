# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseSaleSupplierClient(models.Model):
    _inherit = 'sale.order'

    relation_us = fields.Selection(string='Relación con Nosotros', related='partner_id.relation_us')


class PurchaseSaleSupplierSupplier(models.Model):
    _inherit = 'purchase.order'

    relation_us = fields.Selection(string='Relación con Nosotros', related='partner_id.relation_us')