# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    debit_usd = fields.Monetary(string='Debe($)', currency_field='currency_bs_id', compute='_calculate_debit_usd')
    credit_usd = fields.Monetary(string='Haber($)', currency_field='currency_bs_id', compute='_calculate_credit_usd')
    currency_bs_id = fields.Many2one('res.currency', default = lambda self: self.env['res.currency'].search([('name', '=', 'USD')], limit=1))


    @api.depends('debit')
    def _calculate_debit_usd(self):
        for i in self:
            if i.debit:
                i.debit_usd = self.reajuste_tasa(i, i.debit)
            else:
                i.debit_usd = 0.0


    @api.depends('credit')
    def _calculate_credit_usd(self):
        for i in self:
            if i.credit:
                i.credit_usd = self.reajuste_tasa(i, i.credit)
            else:
                i.credit_usd= 0.0

    def reajuste_tasa(self, i, monto):
        if i.move_id.currency_id.name == 'USD':
            return abs(i.amount_currency)
        if i.move_id.currency_id.name == self.env.company.currency_id.name:
            currency_fac_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        else:
            currency_fac_id = self.env['res.currency'].search([('name', '=', i.move_id.currency_id.name)], limit=1)
        fecha = date.today()
        if i.move_id.invoice_date:
            fecha = i.move_id.invoice_date
        if i.move_id.currency_bs_rate and i.move_id.currency_id.name == self.env.company.currency_id.name:
            rate = 1/i.move_id.currency_bs_rate
        else:
            rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', currency_fac_id.id),
                ('name', '<=', fecha),
            ], limit=1).rate
        if i.move_id.currency_id.name == self.env.company.currency_id.name and rate:
            monto = monto * rate
        if i.move_id.currency_id.name != 'USD' and i.move_id.currency_id.name != self.env.company.currency_id.name:
            monto = (monto) * rate
        return monto


