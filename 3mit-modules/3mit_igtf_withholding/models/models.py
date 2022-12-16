# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import json
from odoo.tools.misc import formatLang

class Company(models.Model):
    _inherit = 'res.company'

    igtf_description = fields.Char(string='Descripción IGTF' )
    igtf_sale_journal_id = fields.Many2one('account.journal', string="Diario de IGTF Ventas", company_dependent=True )
    igtf_purchase_journal_id = fields.Many2one('account.journal', string="Diario de IGTF Compras", company_dependent=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    igtf_description = fields.Char(string='Descripción IGTF', related="company_id.igtf_description", readonly=False,
     help="Descripción del IGTF para añadir a la factura.")



class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    is_igtf = fields.Boolean(string='Aplicar IGTF')
    igtf_percentage = fields.Float(string='3% del Importe')
    igtf_amount = fields.Float(string='3% en Bs')

    @api.onchange('is_igtf')
    def deactivate_igtf(self):
        if self.loc_ven:
            moves = self.env['account.move'].browse(self._context.get('active_ids', []))
            for move in moves:
                if move.move_type in ['out_invoice', 'in_invoice']:
                    if not self.is_igtf:
                        self.igtf_percentage = 0
                        self.igtf_amount = 0
                    else:
                        self.igtf_percentage = round(self.amount * 0.03, 2)
                        self.igtf_amount = self.currency_id._convert(self.igtf_percentage, self.env.company.currency_id,
                                                                     self.env.company, self.payment_date)

    @api.onchange('currency_id')
    def activate_igtf(self):
        if self.loc_ven:
            moves = self.env['account.move'].browse(self._context.get('active_ids', []))
            for move in moves:
                if move.move_type in ['out_invoice', 'in_invoice']:
                    if self.currency_id.id == self.env.company.currency_id.id:
                        self.is_igtf = False
                        self.igtf_percentage = 0
                        self.igtf_amount = 0
                    else:
                        self.is_igtf = True
                        self.igtf_percentage = round(self.amount * 0.03, 2)
                        self.igtf_amount = self.currency_id._convert(self.igtf_percentage, self.env.company.currency_id, self.env.company, self.payment_date)

    @api.onchange('amount')
    def calculate_igtf(self):
        if self.loc_ven and self.is_igtf:
            if self.currency_id.id != self.env.company.currency_id.id:
                self.igtf_percentage = round(self.amount * 0.03, 2)
                self.igtf_amount = self.currency_id._convert(self.igtf_percentage, self.env.company.currency_id,
                                                             self.env.company, self.payment_date)

    def action_create_payments(self):
        if self.is_igtf and self.loc_ven:
            if self._context.get('active_model') == 'account.move':
                move = self.env['account.move'].browse(self._context.get('active_ids', []))
                if move.move_type == 'out_invoice':
                    diario = self.env.company.igtf_sale_journal_id
                    impuesto = self.env['account.tax'].search([('appl_type', '=', 'igtf'),('company_id', '=', self.company_id.id),('type_tax_use', '=', 'sale')])
                if move.move_type == 'in_invoice':
                    diario = self.env.company.igtf_purchase_journal_id
                    impuesto = self.env['account.tax'].search(
                        [('appl_type', '=', 'igtf'), ('company_id', '=', self.company_id.id),('type_tax_use', '=', 'purchase')])
                move.igtf_debt = move.igtf_debt + self.igtf_amount
                move.igtf_usd = move.igtf_usd + self.igtf_percentage
                move.igtf_currency = self.currency_id
                move.is_igtf = True
            vals = {
                'date': self.payment_date,
                'line_ids': False,
                'state': 'draft',
                'journal_id': diario.id,
                'ref': 'IGTF % de ' + move.name,
                'invoice_origin': move.name,
            }
            move_obj = self.env['account.move']
            move_id = move_obj.create(vals)
            move_advance_ = {
                 'account_id': move.partner_id.property_account_receivable_id.id if move.move_type == 'out_invoice' else move.partner_id.property_account_payable_id.id,
                 'company_id': move.company_id.id,
                 'date': self.payment_date,
                 'partner_id': move.partner_id.id,
                 'move_id': move_id.id,
                 'credit': self.igtf_amount if move.move_type == 'in_invoice' else 0.0,
                 'debit': self.igtf_amount if move.move_type == 'out_invoice' else 0.0,
            }

            cuenta = False
            for i in impuesto.invoice_repartition_line_ids:
                if i.account_id:
                    cuenta = i.account_id
            asiento = move_advance_
            move_line_obj = self.env['account.move.line']
            move_line_id1 = move_line_obj.with_context(check_move_validity=False).create(asiento)
            asiento['account_id'] = cuenta.id
            asiento['credit'] = self.igtf_amount if move.move_type == 'out_invoice' else 0.0
            asiento['debit'] = 0.0 if move.move_type == 'out_invoice' else self.igtf_amount
            move_line_id2 = move_line_obj.create(asiento)
            move_id.action_post()
        res = super(AccountPaymentRegister, self).action_create_payments()
        return res

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    igtf_by_group = fields.Binary(string="Tax amount by group",
                                    compute='_compute_invoice_taxes_by_group',
                                    help='Edit Tax amounts if you encounter rounding issues.')
    igtf_by_group_bs = fields.Binary(string="Tax amount by group",
                                  compute='_compute_invoice_taxes_by_group_bs',
                                  help='Edit Tax amounts if you encounter rounding issues.')
    total_with_igtf = fields.Monetary(string='Total con IGTF', copy=False)
    total_with_igtf_bs = fields.Monetary(string='Total con IGTF', copy=False, currency_field='conversion_currency_id')
    igtf_debt = fields.Float(default=0, copy=False)
    igtf_currency = fields.Many2one('res.currency')
    igtf_usd = fields.Float(default=0, copy=False)
    is_igtf = fields.Boolean(default=False, copy=False)
    amount_residual_igtf = fields.Monetary('Importe IGTF Adeudado', store=True, compute='_compute_amount_igtf')


    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id',
                 'currency_id')
    def _compute_invoice_taxes_by_group_bs(self):
        res = super(AccountMoveInherit, self)._compute_invoice_taxes_by_group_bs()
        reconciled_vals = []
        for move in self:
            if move.is_igtf:
                if move.move_type == 'out_invoice':
                    impuesto = self.env['account.tax'].search(
                        [('appl_type', '=', 'igtf'), ('company_id', '=', move.company_id.id),
                         ('type_tax_use', '=', 'sale')])
                if move.move_type == 'in_invoice':
                    impuesto = self.env['account.tax'].search(
                        [('appl_type', '=', 'igtf'), ('company_id', '=', move.company_id.id),
                         ('type_tax_use', '=', 'purchase')])
                group_id = impuesto.tax_group_id
                for partial, amount, counterpart_line in move._get_reconciled_invoices_partials():
                    if counterpart_line.move_id.ref:
                        reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
                    else:
                        reconciliation_ref = counterpart_line.move_id.name

                    reconciled_vals.append({
                        'name': counterpart_line.name,
                        'journal_id': counterpart_line.journal_id.id,
                        'amount': amount,
                        'currency': move.currency_id.symbol,
                        'digits': [69, move.currency_id.decimal_places],
                        'position': move.currency_id.position,
                        'date': counterpart_line.date,
                        'payment_id': counterpart_line.id,
                        'partial_id': partial.id,
                        'account_payment_id': counterpart_line.payment_id.id,
                        'payment_method_name': counterpart_line.payment_id.payment_method_id.name if counterpart_line.journal_id.type == 'bank' else None,
                        'move_id': counterpart_line.move_id.id,
                        'ref': reconciliation_ref,
                    })
                base = 0
                for i in reconciled_vals:
                    pago = self.env['account.payment'].search([('id', '=', i['account_payment_id'])])
                    if pago.currency_id.id != self.env.company.currency_id.id and i['journal_id'] != self.env.company.currency_exchange_journal_id.id and pago.date:
                        base = base + move.currency_id._convert(i['amount'], self.env.company.currency_id, self.env.company, pago.date)
                tax = round(base * 0.03, 2)
                if base and tax:
                    lang_env = self.with_context(lang=move.partner_id.lang).env
                    move.igtf_by_group_bs = [(
                        group_id.name, tax,
                        base,
                        formatLang(lang_env, tax, currency_obj=self.env.company.currency_id),
                        formatLang(lang_env, base, currency_obj=self.env.company.currency_id),
                        1,
                        group_id.id
                    )]
                else:
                    move.igtf_by_group_bs = None
                if move.igtf_by_group_bs:
                    for i in move.igtf_by_group_bs:
                        move.total_with_igtf_bs = move.amount_total_conversion + i[1]
                else:
                    move.total_with_igtf_bs = move.amount_total_conversion
            else:
                for move in self:
                    move.igtf_by_group_bs = None
        return res

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id',
                 'currency_id')
    def _compute_invoice_taxes_by_group(self):
        res = super(AccountMoveInherit, self)._compute_invoice_taxes_by_group()
        reconciled_vals = []
        for move in self:
            if self.env.company.loc_ven and move.is_igtf:
                if move.move_type == 'out_invoice':
                    impuesto = self.env['account.tax'].search(
                        [('appl_type', '=', 'igtf'), ('company_id', '=', move.company_id.id),
                            ('type_tax_use', '=', 'sale')])
                if move.move_type == 'in_invoice':
                    impuesto = self.env['account.tax'].search(
                        [('appl_type', '=', 'igtf'), ('company_id', '=', move.company_id.id),
                            ('type_tax_use', '=', 'purchase')])
                group_id = impuesto.tax_group_id
                
                for partial, amount, counterpart_line in move._get_reconciled_invoices_partials():
                    if counterpart_line.move_id.ref:
                        reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
                    else:
                        reconciliation_ref = counterpart_line.move_id.name

                    reconciled_vals.append({
                        'name': counterpart_line.name,
                        'journal_id': counterpart_line.journal_id.id,

                        'amount': amount,
                        'currency': move.currency_id.symbol,
                        'digits': [69, move.currency_id.decimal_places],
                        'position': move.currency_id.position,
                        'date': counterpart_line.date,
                        'payment_id': counterpart_line.id,
                        'partial_id': partial.id,
                        'account_payment_id': counterpart_line.payment_id.id,
                        'payment_method_name': counterpart_line.payment_id.payment_method_id.name if counterpart_line.journal_id.type == 'bank' else None,
                        'move_id': counterpart_line.move_id.id,
                        'ref': reconciliation_ref,
                    })
                base = 0
                for i in reconciled_vals:
                    pago = self.env['account.payment'].search([('id', '=', i['account_payment_id'])])
                    if pago.currency_id.id != self.env.company.currency_id.id and i['journal_id'] != self.env.company.currency_exchange_journal_id.id:
                        base = base + i['amount']
                tax = round(base * 0.03, 2)
                if base and tax:
                    largo = 1
                    lang_env = self.with_context(lang=move.partner_id.lang).env
                    move.igtf_by_group = [(
                        group_id.name, tax,
                        base,
                        formatLang(lang_env, tax, currency_obj=move.currency_id),
                        formatLang(lang_env, base, currency_obj=move.currency_id),
                        largo,
                        group_id.id
                    )]
                else:
                    move.igtf_by_group = None
                if move.igtf_by_group:
                    for i in move.igtf_by_group:
                        move.total_with_igtf = move.amount_total + i[1]
                    move._compute_amount_igtf()
                else:
                    move.total_with_igtf = move.amount_total
            else:
                for move in self:
                    move.igtf_by_group = None
        return res

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount(self):
        res = super(AccountMoveInherit, self)._compute_amount()
        if self.env.company.loc_ven:
            for move in self:
                if move.igtf_usd:
                    move.payment_state = 'partial'
        return res

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id')
    def _compute_amount_igtf(self):
        for move in self:
            move.amount_residual_igtf = 0.0
            if move.igtf_debt:
                if move.currency_id.id == self.env.company.currency_id.id:
                    move.amount_residual_igtf = move.igtf_debt
                elif move.igtf_currency.id == move.currency_id.id:
                    move.amount_residual_igtf = move.igtf_usd
                else:
                    move.amount_residual_igtf = move.igtf_currency._convert(self.igtf_usd, self.currency_id,
                                                             self.env.company, self.invoice_date)

    @api.model_create_multi
    def create(self, vals):
        res = super(AccountMoveInherit, self).create(vals)
        if self.env.company.loc_ven:
            for i in res:
                if i.move_type in ['out_invoice', 'in_invoice']:
                    i.narration = self.env.company.igtf_description
        return res
