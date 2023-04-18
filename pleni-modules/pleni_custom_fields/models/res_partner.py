# -*- coding: utf-8 -*-
from odoo import models, fields, api
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
        ('07:00', '7:00 am'),
        ('08:00', '8:00 am'),
        ('09:00', '9:00 am'),
        ('10:00', '10:00 am'),
        ('11:00', '11:00 am'),
        ('12:00', '12:00 pm'),
        ('13:00', '1:00 pm'),
        ('14:00', '2:00 pm'),
        ('15:00', '3:00 pm'),
        ('16:00', '4:00 pm'),
        ('17:00', '5:00 pm'), 
    ]

    monday_open = fields.Boolean(string='Lunes Abierto', default=False)
    monday_from = fields.Selection(hours_of_the_day, string="L. Desde")
    monday_to = fields.Selection(hours_of_the_day, string="L. a")
        
    tuesday_open = fields.Boolean(string='Martes Abierto', default=False)
    tuesday_from = fields.Selection(hours_of_the_day, string="M. Desde")
    tuesday_to = fields.Selection(hours_of_the_day, string="M. a")

    wednesday_open = fields.Boolean(string='Miércoles Abierto', default=False)
    wednesday_from = fields.Selection(hours_of_the_day, string="Mi. Desde")
    wednesday_to = fields.Selection(hours_of_the_day, string="Mi. a")

    thursday_open = fields.Boolean(string='Jueves Abierto', default=False)
    thursday_from = fields.Selection(hours_of_the_day, string="J. Desde")
    thursday_to = fields.Selection(hours_of_the_day, string="J. a")

    friday_open = fields.Boolean(string='Viernes Abierto', default=False)
    friday_from = fields.Selection(hours_of_the_day, string="V. Desde")
    friday_to = fields.Selection(hours_of_the_day, string="V. a")

    saturday_open = fields.Boolean(string='Sábado Abierto', default=False)
    saturday_from = fields.Selection(hours_of_the_day, string="S. Desde")
    saturday_to = fields.Selection(hours_of_the_day, string="S. a")

    sunday_open = fields.Boolean(string='Domingo Abierto', default=False)
    sunday_from = fields.Selection(hours_of_the_day, string="D. Desde")
    sunday_to = fields.Selection(hours_of_the_day, string="D. a")

    # sale_order_count = fields.Char(compute='_get_sale_order_count', string='Sale Order Count')

    def _get_day_name(self, delivery_date):
        if not delivery_date:
            return ''
        
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

    # def _get_sale_order_count(self, partner_id):
    #         sale_order_count = self.env['sale.order'].search_count([('partner_id', '=', partner_id.id), ('state', 'not in', ['draft', 'cancel'])])
    #         # return sale_order_count
    #         if sale_order_count > 4:
    #             return "Cliente Nuevo"
    #         else:
    #             return ""

