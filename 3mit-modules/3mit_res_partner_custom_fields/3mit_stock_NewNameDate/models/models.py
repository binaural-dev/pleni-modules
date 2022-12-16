# -*- coding: utf-8 -*-

from asyncio.log import logger
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime


class SaleOrderOnlyDate(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        scheduled_date_view = vals['scheduled_date_view'] if 'scheduled_date_view' in vals else self.scheduled_date_view
        vals['commitment_date'] = scheduled_date_view
        res = super(SaleOrderOnlyDate, self).write(vals)
        if self.scheduled_date_view:
            fecha = str(self.scheduled_date_view)
        else:
            fecha = ''
        if self.am_pm:
            hora = str(self.am_pm)
        else:
            hora = ''
        for picking in self.picking_ids:
            picking.fecha_concatenada_stock = f'{fecha} {hora}'
        for invoice in self.invoice_ids:
            invoice.fecha_concatenada_account = f'{fecha} {hora}'
        return res


class StockPickingOnlyDate(models.Model):
    _inherit = 'stock.picking'

    fecha_concatenada_stock = fields.Char(string='Fecha Programada de Entrega')

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            sale = self.env['sale.order'].search([('name', '=', element['origin'])])
            if sale.scheduled_date_view:
                fecha = sale.scheduled_date_view
            else:
                fecha = ''
            if sale.am_pm:
                hora = sale.am_pm
            else:
                hora = ''
            element['fecha_concatenada_stock'] = f'{fecha} {hora}'
        res = super(StockPickingOnlyDate, self).create(vals_list)
        return res

class AccountMoveRelation(models.Model):
    _inherit = 'account.move'

    fecha_concatenada_account = fields.Char(string='Fecha Programada de Entrega')

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            sale = self.env['sale.order'].search([('name', '=', element['invoice_origin'])])
            if sale.scheduled_date_view:
                fecha = sale.scheduled_date_view
            else:
                fecha = ''
            if sale.am_pm:
                hora = sale.am_pm
            else:
                hora = ''
            element['fecha_concatenada_account'] = f'{fecha} {hora}'
        res = super(AccountMoveRelation, self).create(vals_list)
        return res

