# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import models, fields, api
from datetime import timedelta


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    scheduled_date_view = fields.Date(string='Fecha de Entrega Programada', compute='_compute_only_date'
                                      , store=True)

    am_pm = fields.Selection([('am', 'AM'), ('pm', 'PM')], string="Hora de Entrega")

    @api.depends('commitment_date')
    def _compute_only_date(self):
        for element in self:
            if element.commitment_date and not element.scheduled_date_view:
                element.scheduled_date_view = element.commitment_date
            else:
                element.commitment_date = element.scheduled_date_view


class InheritStockPicking(models.Model):
    _inherit = "stock.picking"

    def _compute_scheduled_date(self):
        res = super(InheritStockPicking, self)._compute_scheduled_date()
        for record in self:
            if record.fecha_concatenada_stock:
                day_hour = record.fecha_concatenada_stock.split(' ')[-1]
                if day_hour == 'am':
                    record.scheduled_date += timedelta(hours=12)
                elif day_hour == 'pm':
                    record.scheduled_date += timedelta(hours=17)
        return res
