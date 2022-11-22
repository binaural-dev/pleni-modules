from asyncio.log import logger
import json
from datetime import date

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
	@http.route(['/home-banners'], type='http', auth="public", website=True, csrf=False)
	def banners_view(self, **kw):
		values = {}
		return request.render("pleni_banners.banners_view", values)