# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    client_notes = fields.Text('Notas del cliente')
