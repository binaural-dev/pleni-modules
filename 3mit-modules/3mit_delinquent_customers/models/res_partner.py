# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    delinquent_check = fields.Boolean('Active Delinquent Payments Limit', help='Activate the delinquent limit feature', default=True)
    # credit_warning = fields.Monetary('Warning Amount')
    # credit_blocking = fields.Monetary('Blocking Amount')
    credit_days = fields.Integer('Credit Days', default=6)  #TODO: hacer que estos dias sean los dias por default de las facturas del ecommerce
    invalid_invoices_qty = fields.Integer('Invalid Invoices', compute='_compute_amount_due')
    amount_due = fields.Monetary('Due Amount', digits='Amount Bs per UT', compute='_compute_amount_due', currency_field='foreign_currency')
    foreign_currency = fields.Many2one('res.currency', string='Foreing Currency', default=lambda self:self.env['res.currency'].browse(2))

    @api.depends('credit', 'debit')
    def _compute_amount_due(self):
        for rec in self:
            if not rec.delinquent_check:
                rec.amount_due = 0
                rec.invalid_invoices_qty = 0
                return
            invalid_invoices = self.env['account.move'].search([('state','=','posted'),('partner_id','=',rec.id),('invoice_date_due','<',date.today()),('payment_state','!=','paid'),('move_type','=','out_invoice')])
            rec.amount_due = sum([inv.amount_residual for inv in invalid_invoices])
            # amount_residual
            rec.invalid_invoices_qty = len(invalid_invoices)


    # @api.constrains('credit_warning', 'credit_blocking')
    # def _check_credit_amount(self):
    #     for credit in self:
    #         if credit.credit_warning > credit.credit_blocking:
    #             raise ValidationError(_('Warning amount should not be greater than blocking amount.'))
    #         if credit.credit_warning < 0 or credit.credit_blocking < 0:
    #             raise ValidationError(_('Warning amount or blocking amount should not be less than zero.'))
