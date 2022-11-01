from asyncio.log import logger
import json
from datetime import date

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
	@http.route(['/my/orders/fault/<int:order_id>'], type='http', auth="public", website=True, csrf=False)
	def faults(self, order_id, access_token=None, **kw):

		not_delivered = []
		pickings = request.env['sale.order.line'].search([('order_id', '=', order_id)])
		for p in pickings:
			if abs(p.product_uom_qty - p.qty_to_invoice) > 0:
				not_delivered.append(p)
		
		values = {
            'pickings': not_delivered
        }

		return request.render("3mit_website_order_new_style.faults_new_style", values)

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