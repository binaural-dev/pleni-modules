# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.misc import formatLang, format_date, get_lang

class AccountTotal(models.Model):
    _inherit = 'account.move'

    conversion = fields.Boolean(default=lambda self: self.currency_id.id != self.env.company.currency_id.id, compute='conversion_state')
    amount_total_conversion = fields.Monetary(string='Total Bs.', currency_field='conversion_currency_id', compute='calculate_amount', store=True)
    amount_untaxed_conversion = fields.Monetary(string='Base Imponible Bs.', currency_field='conversion_currency_id', compute='calculate_amount', store=True)
    conversion_currency_id = fields.Many2one(
        'res.currency',  default=lambda self: self.env.company.currency_id
    )
    amount_tax_conversion = fields.Binary(string="Impuestos",
                                    compute='_compute_invoice_taxes_by_group_bs', currency_field='conversion_currency_id')
    @api.onchange('currency_id')
    def look_over_currency(self):
        if self.currency_id.id == self.env.company.currency_id.id:
            self.conversion = False
        else:
            self.conversion = True
    @api.depends('currency_id')
    def conversion_state(self):
        if self.currency_id.id == self.env.company.currency_id.id:
            self.conversion = False
        else:
            self.conversion = True
    
    def write(self, vals):
        res = super(AccountTotal, self).write(vals)
        if vals.get('currency_bs_rate', False):
            for line in self.line_ids:
                line.with_context(check_move_validity=False)._onchange_price_subtotal()
        return res

    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state')
    def calculate_amount(self):
        for move in self:
            move.amount_untaxed_conversion = move.currency_id._convert(move.amount_untaxed, move.env.company.currency_id, move.env.company, move.date, True, move.currency_bs_rate)
            acumulado = 0
            for i in move.amount_tax_conversion:
                acumulado = acumulado + i[1]
            move.amount_total_conversion = acumulado + move.amount_untaxed_conversion

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id',
                 'currency_id')
    def _compute_invoice_taxes_by_group_bs(self):
        ''' Helper to get the taxes grouped according their account.tax.group.
        This method is only used when printing the invoice.
        '''
        for move in self:
            lang_env = move.with_context(lang=move.partner_id.lang).env
            tax_lines = move.line_ids.filtered(lambda line: line.tax_line_id)
            tax_balance_multiplicator = -1 if move.is_inbound(True) else 1
            res = {}
            # There are as many tax line as there are repartition lines
            done_taxes = set()
            for line in tax_lines:
                res.setdefault(line.tax_line_id.tax_group_id, {'base': 0.0, 'amount': 0.0})
                for i in move.amount_by_group:
                    if i[6] == line.tax_line_id.tax_group_id.id:
                        tasa = 0
                        if i[2]:
                            tasa = round(i[1] / i[2], 2)
                        value = move.currency_id._convert(i[1], self.env.company.currency_id, self.env.company,
                                                          move.date, True, move.currency_bs_rate)
                        res[line.tax_line_id.tax_group_id]['amount'] += value
                        tax_key_add_base = tuple(move._get_tax_key_for_group_add_base(line))
                        if tax_key_add_base not in done_taxes:

                            res[line.tax_line_id.tax_group_id]['base'] += move.currency_id._convert(i[2], self.env.company.currency_id,self.env.company, move.date, True, move.currency_bs_rate)
                    # The base should be added ONCE


            # At this point we only want to keep the taxes with a zero amount since they do not
            # generate a tax line.
            zero_taxes = set()
            for line in move.line_ids:
                for tax in line.tax_ids.flatten_taxes_hierarchy():
                    if tax.tax_group_id not in res or tax.id in zero_taxes:
                        res.setdefault(tax.tax_group_id, {'base': 0.0, 'amount': 0.0})
                        res[tax.tax_group_id]['base'] += tax_balance_multiplicator * (
                            line.amount_currency if line.currency_id else line.balance)

            res = sorted(res.items(), key=lambda l: l[0].sequence)
            for tax in res:
                if tax[0].display_name == "Retención ISLR":
                    line = move.line_ids.filtered(lambda x: x.name == "Retención ISLR Compras")
                    tax[1]["amount"] = - line.credit

            move.amount_tax_conversion = [(
                group.name, amounts['amount'],
                amounts['base'],
                formatLang(lang_env, amounts['amount'], currency_obj=move.conversion_currency_id),
                formatLang(lang_env, amounts['base'], currency_obj=move.conversion_currency_id),
                len(res),
                group.id
            ) for group, amounts in res]

    @api.onchange('invoice_date')
    def reload_prices(self):
        for i in self:
            for line in i.invoice_line_ids:
                line.get_conversion_price()
                line.get_price_subtotal_conversion()


class AccountLineTotal(models.Model):
    _inherit = 'account.move.line'

    conversion = fields.Boolean(related='move_id.conversion')
    conversion_currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id
    )
    price_unit_conversion = fields.Float(string='Precio Bs.')
    price_subtotal_conversion = fields.Monetary(string='Subtotal Bs.', currency_field='conversion_currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountLineTotal, self).create(vals_list)
        for line in res:
            line.get_conversion_price()
            line.get_price_subtotal_conversion()
        return res

    # def _get_computed_price_unit(self):
    #     res = super(AccountLineTotal, self)._get_computed_price_unit()
    #     self.get_conversion_price()
    #     return res

    @api.onchange('product_id','product_uom_id','price_unit')
    def get_conversion_price(self):
        variable = self.currency_id._convert(self.price_unit, self.env.company.currency_id,self.env.company, self.move_id.date, True,self.move_id.currency_bs_rate )
        variable = round(variable, 2)
        if variable and not isinstance(self.move_id.id, models.NewId):
            self.write({'price_unit_conversion': variable})
        else:
            self.price_unit_conversion = variable
        self._write({'price_unit_conversion': variable})


    @api.onchange('product_id', 'product_uom_id', 'price_unit', 'tax_ids', 'quantity')
    def get_price_subtotal_conversion(self):
        price_subtotal_conversion = self.currency_id._convert(self.price_subtotal, self.env.company.currency_id,self.env.company, self.move_id.date, True, self.move_id.currency_bs_rate)
        if price_subtotal_conversion and not isinstance(self.move_id.id, models.NewId):
            self.write({'price_subtotal_conversion': price_subtotal_conversion})
        self._write({'price_subtotal_conversion': price_subtotal_conversion})
