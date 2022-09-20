# coding: utf-8
from odoo import fields, models, api, exceptions
from odoo.http import request
from odoo.exceptions import UserError

class CurrencyRate(models.Model):
    _inherit = 'res.currency.rate'



    _sql_constraints = [
        ('unique_name_per_day', 'Check(1=1)', 'Only one currency rate per day allowed!'),
        ('currency_rate_check', 'CHECK (rate>0)', 'The currency rate must be strictly positive.'),
    ]

class rates(models.Model):
    _inherit = 'res.currency.rate'
    description_rate = fields.Char(string='Descripción')
    name = fields.Datetime(default=lambda self: fields.Datetime.now())
    rate_divided = fields.Float(digits=0, default=1.0, help='The rate of the currency to the currency of rate 1')


    @api.model_create_multi
    def create(self, values):
        if self.loc_ven:
            currency_usd = self.env['res.currency'].search([('name', '=', 'USD')], order='id desc', limit=1)
            last_rate = self.env['res.currency.rate'].search([('currency_id', '=', currency_usd.id)], limit=1,                                           order='name DESC')
            #####
            res = super(rates, self).create(values)
            currency = self.env['res.currency'].search([('id', "=", res.currency_id.id)])
            res.rate_divided = round(res.rate_divided, 2)
            currency.rate = res.rate_divided
            currency.new_rate = res.rate_divided
            res.rate = 1/res.rate_divided
            return res
        else:
            return super(rates, self).create(values)

    def write(self, vals):
        if self.company_id.loc_ven:
            return super(rates, self).write(vals)
        else:
            date = self.name.date()
            datemajor = fields.datetime.combine(date, fields.datetime.max.time())
            dateminor = fields.datetime.combine(date, fields.datetime.min.time())
            tasas = self.env['res.currency.rate'].search([('currency_id', '=', self.currency_id.id),('company_id', '=', self.company_id.id),('name', '<=', datemajor),('name', '>=', dateminor)])
            if tasas:
                if len(tasas) > 1:
                    raise UserError('No puede registrar más de una tasa al día')

            return super(rates, self).write(vals)




    @api.onchange('rate_divided')
    def actualizar_rate(self):
        if self.rate_divided:
            self.rate_divided = round(self.rate_divided, 2)
            self.rate = 1/self.rate_divided
        else:
            self.rate = 0

   


class redirectToRates(models.Model):
    _inherit = 'res.currency'
    new_rate = fields.Float(string="Tasa", readonly=True, default=1)
    make_visible = fields.Boolean(string="User", compute='get_user')


    @api.depends('make_visible')
    def get_user(self, ):
        user_crnt = self._uid
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('3mit_grupo_localizacion.group_localizacion'):
            self.make_visible = True
        else:
            self.make_visible = False

    def _get_rates(self, company, date):
        if not self.ids:
            return {}
        if isinstance(date, str):
            return super(redirectToRates, self)._get_rates(company, date)
        if not (type(date) is fields.datetime):
            date = fields.datetime.combine(date, fields.datetime.max.time())

        self.env['res.currency.rate'].flush(['rate', 'currency_id', 'company_id', 'name'])
        query = """SELECT c.id,
                          COALESCE((SELECT r.rate FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC, r.write_date desc 
                                  LIMIT 1), 1.0) AS rate
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company.id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        return currency_rates

    def _convert(self, from_amount, to_currency, company, date, round=True, currency_bs_rate=0):
        if self.id == 2 and self.id != to_currency.id and self.make_visible:
            factura = None
            if currency_bs_rate != 0:
                to_amount = from_amount * currency_bs_rate
                return to_currency.round(to_amount) if round else to_amount
            id = request
            if request.params.get('model') == 'purchase.order':
                if request.params.get('method') == 'button_confirm' or request.params.get('method') == 'action_create_invoice':
                    po_id = request.params.get('args')[0]
                    purchase_order = self.env['purchase.order'].search([('id', '=', po_id)], limit=1)
                    tasa = purchase_order.new_currency_bs_rate
                    to_amount = from_amount * tasa
                    return to_currency.round(to_amount) if round else to_amount
            if request.params.get('model') == 'account.move.line':
                factura = request.params.get('args')[1].get('move_id')
                if factura.get('currency_bs_rate'):
                    to_amount = from_amount * factura.get('currency_bs_rate')
                    return to_currency.round(to_amount) if round else to_amount
                else:
                    return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)
            elif request.params.get('model') == 'account.move':
                if request.params.get('method') == 'action_post' or request.params.get('method') == 'read' or request.params.get('method') == 'button_draft' or request.params.get('method') == 'button_cancel':
                    factura = request.params.get('args')[0][0]
                else:
                    if id.params.get('args')[0]:
                        factura = id.params.get('args')[0]
                        if type(factura) == dict:
                            currency_bs_rate = request.params.get('args')[0].get('currency_bs_rate')
                            to_amount = from_amount * currency_bs_rate
                            return to_currency.round(to_amount) if round else to_amount
                        if type(factura) == list:
                            factura = self.env['account.move'].search([('id', "=", factura[0])])
                            if factura.currency_bs_rate:
                                to_amount = from_amount * factura.currency_bs_rate
                                return to_currency.round(to_amount) if round else to_amount
                            else:
                                return super(redirectToRates, self)._convert(from_amount, to_currency, company, date,
                                                                             round)
                    else:
                        if id.params.get('args')[1] and id.params.get('args')[1].get('invoice_origin'):
                            purchase = id.params.get('args')[1].get('invoice_origin')
                            # if
                            purchase = self.env['purchase.order'].search(
                                [('name', '=', purchase)], limit=1)
                            if purchase and purchase.new_currency_bs_rate != 0.00:
                                id.params.get('args')[1].update({
                                    'currency_bs_rate': purchase.new_currency_bs_rate
                                })
                                to_amount = from_amount * purchase.new_currency_bs_rate
                                return to_currency.round(to_amount) if round else to_amount
                        else:
                            currency_bs_rate = request.params.get('args')[1].get('currency_bs_rate')
                            to_amount = from_amount * currency_bs_rate
                            return to_currency.round(to_amount) if round else to_amount
                if factura:
                    if type(factura) == int:
                        factura = self.env['account.move'].search([('id', "=", factura)])
                        if factura.currency_bs_rate:
                            to_amount = from_amount * factura.currency_bs_rate
                            return to_currency.round(to_amount) if round else to_amount
                        else:
                            return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)
                    else:
                        if not factura.get('invoice_origin'):
                            if factura.get('currency_bs_rate'):
                                to_amount = from_amount * factura.get('currency_bs_rate')
                                return to_currency.round(to_amount) if round else to_amount
                            else:
                                return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)
                        else:
                            purchase = factura.get('invoice_origin')
                            tasa_purchase = self.env['purchase.order'].search([('name', '=', purchase)], limit=1).new_currency_bs_rate
                            if tasa_purchase and tasa_purchase != 0:
                                factura.write({'currency_bs_rate': tasa_purchase})
                                to_amount = from_amount * tasa_purchase
                                return to_currency.round(to_amount) if round else to_amount
                            else:
                                return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)
                else:
                    return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)
            else:
                return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)
        else:
            return super(redirectToRates, self)._convert(from_amount, to_currency, company, date, round)