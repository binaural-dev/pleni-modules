# -*- coding: utf-8 -*-

import logging
from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.exceptions import UserError, ValidationError


class WebsiteSaleDeliveryInherit(WebsiteSaleDelivery):

	@http.route(['/shop/payment'], type='http', auth="public", website=True)
	def payment(self, **post):
		response = super(WebsiteSaleDelivery, self).payment(**post)
		order = request.website.sale_get_order()
		delivery_lines = request.env['sale.order.line'].sudo().search([('name','ilike','delivery'),('order_id','=',order.id)])
		delivery_lines.sudo().unlink()
		carrier = request.env['delivery.carrier'].sudo().search([('active','=',True)],limit=1)
		if carrier and not order.amount_delivery :
			order.carrier_id = carrier.id
			order.amount_delivery = carrier.fixed_price if order.amount_total < carrier.amount else 0
		return response
	
	@http.route()
	def payment_transaction(self, *args, **kwargs):
		order = request.website.sale_get_order()
		order.delivery_set = True
		return super(WebsiteSaleDeliveryInherit, self).payment_transaction(*args, **kwargs)