# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    cancellation_reasons = fields.Selection([
        ('cancellation', 'Cancelación'),
        ('refund', 'Devolución'),
        ('failure', 'Falla')], string="Razones de cancelación")

    cancellation_types = fields.Selection([
        ('prices', 'Precios'),
        ('delivery_times', 'Tiempos de entrega'),
        ('others', 'Otros')], string="Motivo de la cancelación")

    refund_types = fields.Selection([
        ('bad_quality', 'Calidad no conforme'),
        ('prefer_another', 'Preferencias de selección'),
        ('others', 'Otros')], string="Motivo de la devolución")

    failure_types = fields.Selection([
        ('inventory_fail', 'Falla inventario'),
        ('operation_fail', 'Falla operaciones'),
        ('others', 'Otros')], string="Motivo de la falla")
