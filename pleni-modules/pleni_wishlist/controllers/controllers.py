# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import http, api, SUPERUSER_ID
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale
import json
from datetime import date
import re


class AddOrderLines(http.Controller):
    @http.route('/addOrderLines', auth='public', type='json', website='True')
    def add_order_lines(self, website_wishlist_product, **kwarg):
        string = self.list_int(website_wishlist_product)
        if not website_wishlist_product: return False
        products = request.env['product.wishlist'].sudo().browse(string)
        print(products)
        order = request.website.sale_get_order(force_create=1)
        orderLines = [line.product_id.id for line in order.order_line]
        for element in products:
            if element.product_id.id in orderLines:
                line = request.env['sale.order.line'].sudo().search([('order_id', '=', order.id),
                                                                    ('product_id', '=', element.product_id.id)])
                line.write({
                    'product_uom_qty': line.product_uom_qty + 1
                })
                continue
            values = {
                'product_id': element.product_id.id,
                'order_id': order.id,
                'name': element.product_id.name,
                'product_uom_qty': 1,
                'price_unit': element.price,
            }

            request.env['sale.order.line'].sudo().create(values)
        return True

    def list_int(self, lista):
        characters = "[]"
        string = ''.join(x for x in lista if x not in characters)
        string = string.split(',')
        for i in range(len(string)):
            string[i] = int(string[i])
        return string
