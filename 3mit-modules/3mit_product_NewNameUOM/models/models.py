# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class pruebaFormulario(models.Model):
    _inherit = 'product.template'

    prueba = fields.Char(string='Campo prueba')



