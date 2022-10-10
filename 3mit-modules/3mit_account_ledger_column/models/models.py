# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    balance_usd = fields.Monetary(string='Saldo(Bs)', currency_field='currency_bs_id', store=True, compute='_calculate_balance_usd')

    @api.depends('debit_usd', 'credit_usd')
    def _calculate_balance_usd(self):
        for line in self:
            line.balance_usd = line.debit_usd - line.credit_usd
