# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    times_sold = fields.Integer('Times sold', default=0)
