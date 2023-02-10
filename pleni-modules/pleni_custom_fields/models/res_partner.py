# -*- coding: utf-8 -*-
from odoo import models, fields


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
    monday_open = fields.Boolean(string='Lunes Abierto', default=False)
    monday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    monday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")
        
    tuesday_open = fields.Boolean(string='Martes Abierto', default=False)
    tuesday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    tuesday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")

    wednesday_open = fields.Boolean(string='Miércoles Abierto', default=False)
    wednesday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    wednesday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")

    thursday_open = fields.Boolean(string='Jueves Abierto', default=False)
    thursday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    thursday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")

    friday_open = fields.Boolean(string='Viernes Abierto', default=False)
    friday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    friday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")

    saturday_open = fields.Boolean(string='Sábado Abierto', default=False)
    saturday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    saturday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")

    sunday_open = fields.Boolean(string='Domingo Abierto', default=False)
    sunday_from = fields.Selection(
        [
            ('7:00am', '7:00am'),
            ('8:00am', '8:00am'),
            ('9:00am', '9:00am'),
            ('10:00am', '10:00am'),
            ('11:00am', '11:00am')
        ], string="Desde")
    sunday_to = fields.Selection(
    [
            ('12:00pm', '12:00pm'),
            ('1:00pm', '1:00pm'),
            ('2:00pm', '2:00pm'),
            ('3:00pm', '3:00pm'),
            ('4:00pm', '4:00pm'),
            ('5:00pm', '5:00pm'), 
    ], string="a")