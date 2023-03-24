# -*- coding: utf-8 -*-

from odoo import http, fields, _
from odoo.http import request
import base64
import json

class SaleOrderInfo(http.Controller):
    @http.route('/api/v1/sale_order/info/<int:sale_order_id>', type='http', auth="none", methods=['GET'])
    def sale_order_info(self, sale_order_id):
        sale_order = request.env['sale.order'].sudo().search([('id', '=', sale_order_id)])

        order = {
            'id': sale_order.id,
            'name': sale_order.name,
            # 'date_order': sale_order.date_order,
            'amount_total': sale_order.amount_total
        }

        return json.dumps(order)
        # if sale_order:
        #     return {
        #         "code": 200,
        #         "sale_order": {
        #             "id": sale_order.id,
        #             "name": sale_order.name,
        #             'metadata': sale_order.read()
        #         }
        #     }
        # else:
        #     return {
        #         "code": 404,
        #         "error": "Sale Order not found"
        #     }
        
    @http.route('/api/v1/sale_order', type='http', auth="none", methods=['GET'])
    # Get all sale orders ids
    def sale_order(self):
        sale_orders = request.env['sale.order'].sudo().search([])
        sale_orders_ids = []
        for sale_order in sale_orders:
            sale_orders_ids.append(sale_order.id)
        return json.dumps({"asas": sale_orders_ids})
        # return {
        #     "code": 200,
        #     "sale_orders": sale_orders_ids
        # }
        
    # Update sale order status
    # @http.route('/api/v1/sale_order/update_status', type='http', auth="api_key", methods=['POST'], csrf=False)
    # def sale_order_update_status(self, id, status):
    #     sale_order = request.env['sale.order'].search([('id', '=', id)])
    #     if sale_order:
    #         sale_order.write({
    #             'state': status
    #         })
    #         return {
    #             "code": 200,
    #             "sale_order": {
    #                 "id": sale_order.id,
    #                 "name": sale_order.name,
    #                 'metadata': sale_order.read()
    #             }
    #         }
    #     else:
    #         return {
    #             "code": 404,
    #             "error": "Sale Order not found"
    #         }