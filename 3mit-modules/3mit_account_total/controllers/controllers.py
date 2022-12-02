# -*- coding: utf-8 -*-
# from odoo import http


# class 3mitAccountTotal(http.Controller):
#     @http.route('/3mit_account_total/3mit_account_total/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/3mit_account_total/3mit_account_total/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('3mit_account_total.listing', {
#             'root': '/3mit_account_total/3mit_account_total',
#             'objects': http.request.env['3mit_account_total.3mit_account_total'].search([]),
#         })

#     @http.route('/3mit_account_total/3mit_account_total/objects/<model("3mit_account_total.3mit_account_total"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('3mit_account_total.object', {
#             'object': obj
#         })
