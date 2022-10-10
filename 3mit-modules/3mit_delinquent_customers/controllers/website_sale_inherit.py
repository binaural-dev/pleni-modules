from asyncio.log import logger
import json
from datetime import date

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
	@http.route(['/shop/checkout'], type='http', auth="user", website=True, sitemap=False)
	def checkout(self, **post):
		order = request.website.sale_get_order()

		partner = request.env['res.partner'].browse(order.partner_id.id)
		invalid_invoices = request.env['account.move'].search([('state','=','posted'),('partner_id','=',partner.id),('invoice_date_due','<',date.today())])
		amount_due = sum([inv.amount_total for inv in invalid_invoices])

		values = self.checkout_values(**post)

		if partner.delinquent_check:
			# msg = ''
			# if partner.invalid_invoices_limit <= partner.invalid_invoices_qty:
			# 	msg = 'Customer has 2 o more unpayed invoices.'
			# elif partner.credit_blocking <= amount_due:
			# 	msg = 'Customer credit limit exceeded.'
			
			if partner.invalid_invoices_qty:
				values.update({'due': amount_due, 'order': order, 'invalid_invoices_qty': len(invalid_invoices)})
				return request.render("3mit_delinquent_customers.delinquent_customer_error", values)

		redirection = self.checkout_redirection(order)
		if redirection:
			return redirection

		if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
			return request.redirect('/shop/address')

		redirection = self.checkout_check_address(order)
		if redirection:
			return redirection


		if post.get('express'):
			return request.redirect('/shop/confirm_order')

		values.update({'website_sale_order': order})

		# Avoid useless rendering if called in ajax
		if post.get('xhr'):
			return 'ok'
		return request.render("website_sale.checkout", values)