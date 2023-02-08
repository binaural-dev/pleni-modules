# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.http import request
import base64


class OrderPayment(http.Controller):
    @http.route('/webhook/v1/order_payment', type='json', auth="api_key", methods=['POST'], csrf=False)
    def order_payment(self, method, partner_id, amount, date):
        bank = None
        if method == 'Zelle' or method == 'Stripe':
            bank = 'Bank of America'
        if method == 'C2P' or method == 'Pago Movil':
            bank = 'Bancamiga'

        payment = request.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            # 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'partner_id': partner_id,
            'amount': amount,
            'currency_id': int(request.env['res.currency'].search([('name', '=', 'USD')]).id),
            'date': fields.Date.from_string(date),
            'journal_id': int(request.env['account.journal'].search([('name', 'ilike', bank)]).id)
        })
        print(payment.read())
        return {
            "code": 200,
            "payment": {
                "id": payment.id,
                "name": payment.name,
                'metadata': payment.read()
            }
            # "paymentID": payment_id,
            # "paymentName": payment_name
        }

    # def _default_currency_rate(self):
    #     rate = 0
    #     alternate_currency = int(
    #         request.env['ir.config_parameter'].sudo().get_param('curreny_foreign_id'))
    #     if alternate_currency:
    #         currency = request.env['res.currency.rate'].search(
    #             [('currency_id', '=', alternate_currency)], limit=1, order='name desc')
    #         if currency:
    #             rate = currency.rate if currency.currency_id.name == 'VEF' else currency.vef_rate

    #     return rate
