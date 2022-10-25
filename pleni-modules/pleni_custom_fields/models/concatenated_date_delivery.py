# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
from re import search


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

        if (len(self.picking_ids) < 1):
            for picking in self.picking_ids:
                picking.scheduled_date_stock = date_delivery_view
                picking.am_pm = am_pm

        for invoice in self.invoice_ids:
            invoice.scheduled_date_account = date_delivery_view
            invoice.am_pm = am_pm

        res = super(SaleOrderInherit, self).write(vals)
        return res


class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    scheduled_date_stock = fields.Date(string='Fecha Programada de Entrega')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], string="Bloque de Hora de Entrega")

    @api.model_create_multi
    def create(self, vals_list):

        INCOMING_PICKING = 1
        OUTCOMING_PICKING = 2

        for element in vals_list:
            sale = self.env['sale.order'].search(
                [('name', '=', element['origin'])])

            # When a backorder is created, an extra day is added to the scheduled delivery date.
            if (self and 'backorder_id' in element):
                element['scheduled_date_stock'] = sale.date_delivery_view + \
                    timedelta(days=1)
                element['am_pm'] = sale.am_pm
            # When a return is created, an extra day is added to the scheduled delivery date.
            elif (self and 'picking_type_id' in element and element['picking_type_id'] == INCOMING_PICKING):
                element['scheduled_date_stock'] = element['scheduled_date_stock']
                element['am_pm'] = element['am_pm']
            # When a re-return is created, an extra day is added to scheduled delivert date based into date field.
            elif (self and ('picking_type_id' in element and element['picking_type_id'] == OUTCOMING_PICKING) and search('IN', element['origin'])):
                element['scheduled_date_stock'] = element['date'] + \
                    timedelta(days=1)
                element['am_pm'] = element['am_pm']
            else:
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
        string='Fecha Programada de Entrega', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['scheduled_date_report'] = ", s.date_delivery_view as scheduled_date_report"
        groupby += ', s.date_delivery_view'
        return super(SaleReportInherit, self)._query(with_clause, fields, groupby, from_clause)
