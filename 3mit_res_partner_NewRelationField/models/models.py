# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    relation_us = fields.Selection(selection=[('client', 'Cliente'), ('supplier', 'Proveedor'), ('both', 'Cliente-Proveedor'),
                                              ('seller','Vendedor')], string="Relación con Nosotros")



