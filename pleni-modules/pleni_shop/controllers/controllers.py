# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import http, api, SUPERUSER_ID
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale
import json


class GetUomFactor(http.Controller):
	@http.route('/getUomFactor', auth='none', type='json', cors='*')
	def get_uom_factor(self, uom_id, **kwarg):
		if not uom_id: return False
		factor = request.env['uom.uom'].sudo().browse(uom_id).factor
		return factor

	@http.route('/getBiggestUom', auth='none', type='json', cors='*')
	def get_biggest_uom(self, uoms, **kwarg):
		if not len(uoms): return False
		uoms = request.env['uom.uom'].sudo().search([('id', 'in', uoms)], order= 'factor asc')
		uom_ids = []
		for item in uoms:
			uom_ids.append(item.name)
		return uom_ids


class GetDisplayPrice(http.Controller):
	@http.route('/getDisplayPrice', auth='none', type='json', cors='*')
	def get_display_price(self, add_qty, product_id, product_template_id, pricelist_id, **kwarg):
		if product_template_id:
			product_id = request.env['product.product'].sudo().search([('product_tmpl_id','=',int(product_template_id))]).id
		pricelist_items = request.env['product.pricelist.item'].sudo().search([('pricelist_id','=',int(pricelist_id)),'|',('product_tmpl_id','=',int(product_template_id)),('product_id','=',int(product_id))], order= 'min_quantity asc')
		price=0
		for item in pricelist_items:
			if float(add_qty) >= item.min_quantity:
				price = item.fixed_price
		return price*float(add_qty)

class GetProductPricelist(WebsiteSale):
	@http.route('/getProductPricelist', type='json', auth="public", website=True)
	def get_product_Pricelist(self, **kwarg):
		order = request.website.sale_get_order()
		return order.pricelist_id.id
