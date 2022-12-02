# coding: utf-8
from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date, timedelta

class SaleOrderInherit(models.Model):
    _inherit = 'account.move'

    currency_bs_rate = fields.Float(string='Tasa($)', store=True, default=lambda self: self.env['res.currency.rate'].search([('currency_id.name', '=', 'USD')], order='name desc', limit=1).rate_divided)
    currency_bs_date = fields.Date(string="Fecha")

    @api.onchange('invoice_date')
    def calculate_last_rate(self):
        for i in self:
            fecha = None
            if i.invoice_date:
                fecha = i.invoice_date
            else:
                fecha = date.today()
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', currency_id.id),
                ('name', '<=', fecha),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
            if rate.rate != 0 or rate.rate:
                if not i.invoice_origin:
                    i.currency_bs_rate = rate.rate_divided
                else:
                    if i.move_type == 'in_invoice':
                        purchase = self.env['purchase.order'].search([('name', '=', i.invoice_origin)])
                        if purchase.fixed_rate_boolean:
                            i.currency_bs_rate = purchase.new_currency_bs_rate
                        else:
                            i.currency_bs_rate = rate.rate_divided
                    else:
                        i.currency_bs_rate = rate.rate_divided
            else:
                if i.invoice_origin:
                    if i.move_type == 'in_invoice':
                        purchase = self.env['purchase.order'].search([('name', '=', i.invoice_origin)])
                        if purchase.fixed_rate_boolean:
                            i.currency_bs_rate = purchase.new_currency_bs_rate
                        else:
                            i.currency_bs_rate = 0
                    else:
                        i.currency_bs_rate = 0
                else:
                    i.currency_bs_rate = 0
            i.currency_bs_date = rate.name

    @api.onchange('currency_bs_rate', 'invoice_date')
    def onchange_date_apply(self):
        self._write({'currency_bs_rate': self.currency_bs_rate})
        for line in self.line_ids:
            line._get_fields_onchange_subtotal()






