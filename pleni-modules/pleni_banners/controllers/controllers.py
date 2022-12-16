# -*- coding: utf-8 -*-
from odoo import http


class PleniBanners(http.Controller):
    @http.route('/pleni_banners/pleni_banners/', auth='public')
    def view_banner(self, order_id, access_token=None, **kw):
        values = {}
        return request.render("pleni_banners.banners_view", values)
    # def index(self, **kw):
    #     return "Hello, world"

    @http.route('/pleni_banners/pleni_banners/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('pleni_banners.listing', {
            'root': '/pleni_banners/pleni_banners',
            'objects': http.request.env['pleni_banners.pleni_banners'].search([]),
        })

    @http.route('/pleni_banners/pleni_banners/objects/<model("pleni_banners.pleni_banners"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('pleni_banners.object', {
            'object': obj
        })
