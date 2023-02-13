# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import datetime

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    PURCHASE_FREQUENCY = [
        ('weekly_recurring', 'Recurrente semanal'),
        ('recurring_fortnightly', 'Recurrente quincenal'),
        ('monthly_recurring', 'Recurrente mensual'),
        ('eventual', 'Eventual')
    ]

    commercial_name = fields.Char(string='Nombre comercial')
    dispatcher_instructions = fields.Char(
        string='Instrucciones para el despachador')
    ref_point = fields.Char(string='Centro Comercial/Empresarial')
    urbanization_area = fields.Many2one(
        'urbanization.area', string='Zona/Urbanización')
    purchase_frequency = fields.Selection(
        PURCHASE_FREQUENCY, string='Frecuencia de compra')
    how_find_us = fields.Many2one('find.us', string='¿Cómo llegó a nosotros?')
    fiscal_invoice_needed = fields.Boolean(string='FF')
    plus_code_location = fields.Char(string='Plus code (Location)')
    trained_salesperson = fields.Many2one(
        'res.users', string='Vendedor entrenador')
    trained_person = fields.Many2one(
        'res.partner', string='[Deprecated] Vendedor')
    relation_us = fields.Selection(selection=[('client', 'Cliente'), ('supplier', 'Proveedor'), ('both', 'Cliente-Proveedor'),
                                              ('seller','Vendedor')], string="Relación con Nosotros")

    hours_of_the_day = [
        ('7:00am', '7:00am'),
        ('8:00am', '8:00am'),
        ('9:00am', '9:00am'),
        ('10:00am', '10:00am'),
        ('11:00am', '11:00am'),
        ('12:00pm', '12:00pm'),
        ('1:00pm', '1:00pm'),
        ('2:00pm', '2:00pm'),
        ('3:00pm', '3:00pm'),
        ('4:00pm', '4:00pm'),
        ('5:00pm', '5:00pm'), 
    ]

    monday_open = fields.Boolean(string='Lunes Abierto', default=False)
    monday_from = fields.Selection(hours_of_the_day, string="Desde")
    monday_to = fields.Selection(hours_of_the_day, string="a")
        
    tuesday_open = fields.Boolean(string='Martes Abierto', default=False)
    tuesday_from = fields.Selection(hours_of_the_day, string="Desde")
    tuesday_to = fields.Selection(hours_of_the_day, string="a")

    wednesday_open = fields.Boolean(string='Miércoles Abierto', default=False)
    wednesday_from = fields.Selection(hours_of_the_day, string="Desde")
    wednesday_to = fields.Selection(hours_of_the_day, string="a")

    thursday_open = fields.Boolean(string='Jueves Abierto', default=False)
    thursday_from = fields.Selection(hours_of_the_day, string="Desde")
    thursday_to = fields.Selection(hours_of_the_day, string="a")

    friday_open = fields.Boolean(string='Viernes Abierto', default=False)
    friday_from = fields.Selection(hours_of_the_day, string="Desde")
    friday_to = fields.Selection(hours_of_the_day, string="a")

    saturday_open = fields.Boolean(string='Sábado Abierto', default=False)
    saturday_from = fields.Selection(hours_of_the_day, string="Desde")
    saturday_to = fields.Selection(hours_of_the_day, string="a")

    sunday_open = fields.Boolean(string='Domingo Abierto', default=False)
    sunday_from = fields.Selection(hours_of_the_day, string="Desde")
    sunday_to = fields.Selection(hours_of_the_day, string="a")

    def _get_day_name(self, delivery_date):
        day = delivery_date.strftime("%A")
        
        if day == 'Monday' and self.monday_open:
            return f'Lunes: {self.monday_from}-{self.monday_to}'

        if day == 'Tuesday' and self.tuesday_open:
            return f'Martes: {self.tuesday_from}-{self.tuesday_to}'
        
        if day == 'Wednesday' and self.wednesday_open:
            return f'Miércoles: {self.wednesday_from}-{self.wednesday_to}'
                
        if day == 'Thursday' and self.thursday_open:
            return f'Jueves: {self.thursday_from}-{self.thursday_to}'

        if day == 'Friday' and self.friday_open:
            return f'Viernes: {self.friday_from}-{self.friday_to}'

        if day == 'Saturday' and self.saturday_open:
            return f'Sábado: {self.saturday_from}-{self.saturday_to}'

        if day == 'Sunday' and self.sunday_open:
            return f'Domingo: {self.sunday_from}-{self.sunday_to}'
        
        return ''
