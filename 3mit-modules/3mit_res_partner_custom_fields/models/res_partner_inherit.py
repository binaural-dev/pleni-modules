# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    commercial_name = fields.Char(string='Nombre comercial')
    dispatcher_instructions = fields.Char(string='Instrucciones para el despachador')
    ref_point = fields.Char(string='Centro Comercial/Empresarial')
    urbanization_area = fields.Many2one('urbanization.area', string='Zona/Urbanización')
    purchase_frequency = fields.Selection(selection=[('weekly_recurring', 'Recurrente semanal'), ('recurring_fortnightly', 'Recurrente quincenal'),
                                                     ('monthly_recurring', 'Recurrente mensual'), ('eventual', 'Eventual')],
                                          string='Frecuencia de compra')
    how_find_us = fields.Many2one('find.us', string='¿Cómo llegó a nosotros?')
    fiscal_invoice_needed = fields.Boolean(string='FF')
    plus_code_location = fields.Char(string='Plus code (Location)')
    trained_salesperson = fields.Many2one('res.users', string='Vendedor entrenador')
    trained_person = fields.Many2one('res.partner', string='Vendedor')
