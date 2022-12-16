# coding: utf-8
from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date, timedelta

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    currency_bs_rate = fields.Float(string='Tasa($)', store=True, compute="calculate_last_rate", default=lambda self: self.env['res.currency.rate'].search([('currency_id.name', '=', 'USD')], order='name desc', limit=1).rate_divided)
    currency_bs_date = fields.Datetime(string="Fecha")

    @api.depends('date_order')
    def calculate_last_rate(self):
        for i in self:
            fecha = None
            if i.date_order:
                fecha = i.date_order.date()
            else:
                fecha = date.today()
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', currency_id.id),
                ('name', '<=', fecha),
            ], limit=1)
            i.currency_bs_rate = rate.rate_divided
            i.currency_bs_date = rate.name

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    currency_bs_rate = fields.Float(string='Tasa($)', store=True, compute="calculate_last_rate")
    currency_bs_date = fields.Datetime(string="Fecha")

    @api.depends('date_order')
    def calculate_last_rate(self):
        for i in self:
            fecha = None
            if i.date_order:
                fecha = i.date_order.date()
            else:
                fecha = date.today()
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', currency_id.id),
                ('name', '<=', fecha),
            ], limit=1)
            i.currency_bs_rate = rate.rate
            i.currency_bs_date = rate.name



