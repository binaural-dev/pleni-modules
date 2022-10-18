# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    date_delivery_view = fields.Date(
        string='Fecha Programada de Entrega', compute='_compute_only_date', store=True)
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.depends('commitment_date')
    def _compute_only_date(self):
        for element in self:
            if element.commitment_date and not element.date_delivery_view:
                element.date_delivery_view = element.commitment_date
            else:
                element.commitment_date = element.date_delivery_view

    def write(self, vals):
        date_delivery_view = vals['date_delivery_view'] if 'date_delivery_view' in vals else self.date_delivery_view
        am_pm = vals['am_pm'] if 'am_pm' in vals else self.am_pm
        vals['commitment_date'] = date_delivery_view
        res = super(SaleOrderInherit, self).write(vals)
        for picking in self.picking_ids:
            picking.scheduled_date_stock = date_delivery_view
            picking.am_pm = am_pm
        for invoice in self.invoice_ids:
            invoice.scheduled_date_account = date_delivery_view
            invoice.am_pm = am_pm
        return res


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    scheduled_date_stock = fields.Date(string='Fecha Programada de Entrega')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    # def _compute_scheduled_date(self):
    #     res = super(StockPickingInherit, self)._compute_scheduled_date()
    #     for record in self:
    #         if record.fecha_concatenada_stock:
    #             day_hour = record.fecha_concatenada_stock.split(' ')[-1]
    #             if day_hour == 'am':
    #                 record.scheduled_date += timedelta(hours=12)
    #             elif day_hour == 'pm':
    #                 record.scheduled_date += timedelta(hours=17)
    #     return res

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            sale = self.env['sale.order'].search(
                [('name', '=', element['origin'])])
            element['scheduled_date_stock'] = sale.date_delivery_view
            element['am_pm'] = sale.am_pm
        res = super(StockPickingInherit, self).create(vals_list)
        return res


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    scheduled_date_account = fields.Date(
        string='Fecha Programada de Entrega')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            if 'invoice_origin' in element:
                sale = self.env['sale.order'].search(
                    [('name', '=', element['invoice_origin'])])
                element['scheduled_date_account'] = sale.date_delivery_view
                element['am_pm'] = sale.am_pm
        res = super(AccountMoveInherit, self).create(vals_list)
        return res


class SaleReportInherit(models.Model):
    _inherit = 'sale.report'

    scheduled_date_report = fields.Date(
        string='Fecha Programada de Entrega')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            sale = self.env['sale.order'].search(
                [('id', '=', element['order_id'])])
            element['scheduled_date_report'] = sale.date_delivery_view
            element['am_pm'] = sale.am_pm
        res = super(SaleReportInherit, self).create(vals_list)
        return res