# -*- coding: utf-8 -*-

from odoo import http, fields, _
from odoo.http import request
import base64
import json

# Dictionary for payment status
payment_status = [
    'pending',
    'verified',
    'partial',
    'not_verified',
]

# Dictionary for payment methods
payment_methods = {
    'cash': 14,
    'stripe': 29,
    'pagomovil': 15,
    'zelle': 19,
    'pos': 16,
    'transferBs': 17,
    'transferUSD': 18,
    'c2p': 34
}

class SaleOrderInfo(http.Controller):
    @http.route('/api/v1/sale_order/info/<int:sale_order_id>', type='http', auth="none", methods=['GET'])
    def sale_order_info(self, sale_order_id):
        sale_order = request.env['sale.order'].sudo().search([('id', '=', sale_order_id)])

        order = {
            "id": sale_order.id,
            "name": sale_order.name,
            "payment_state": sale_order.payment_state,
            "payment_methods": sale_order.payment_methods.name
        }

        return json.dumps(order)
        
    # @http.route('/api/v1/sale_order', type='http', auth="none", methods=['GET'])
    # # Get all sale orders ids
    # def sale_order(self):
    #     sale_orders = request.env['sale.order'].sudo().search([])
    #     sale_orders_ids = []
    #     for sale_order in sale_orders:
    #         sale_orders_ids.append(sale_order.id)
    #     return json.dumps({"asas": sale_orders_ids})
    #     # return {
    #     #     "code": 200,
    #     #     "sale_orders": sale_orders_ids
    #     # }
        
    #Update sale order status
    @http.route('/api/sale_order/update_state/<int:id>', type='json', auth="none", methods=['POST'])
    def sale_order_update_state(self, id):
        if not id:
            return {
                "code": 400,
                "message": "Sale order id is required"
            }
        # Get sale order
        sale_order = request.env['sale.order'].sudo().search([('id', '=', id)])

        # Get body data
        data = request.jsonrequest
        payment_state = data['payment_state']
        payment_method = data['payment_method']
        acquirer_id = payment_methods[payment_method]
        # acquirer_id = data['acquirer_id']

        # If not payment state
        if not payment_state:
            return {
                "code": 400,
                "message": "Payment state is required"
            }
        
        # If not any of the dictionary
        if payment_state not in payment_status:
            return {
                "code": 400,
                "message": "Payment state is not valid"
            }
        
        # If not payment method
        if not acquirer_id:
            return {
                "code": 400,
                "message": "Payment method is required"
            }

        
        if sale_order:
            sale_order.write({
                'payment_state': payment_state,
                'payment_methods': [(1, acquirer_id)]
                # 'payment_methods': acquirer_id,
            })
            updated_sale_order = request.env['sale.order'].sudo().search([('id', '=', id)])
            return {
                "code": 200,
                "message": "Sale order updated",
                "sale_order": {
                    "id": updated_sale_order.id,
                    "name": updated_sale_order.name,
                    "payment_state": updated_sale_order.payment_state,
                    "payment_methods": updated_sale_order.payment_methods.name
                }
            }
        else:
            return {
                "code": 404,
                "message": "Sale order not found"
            }