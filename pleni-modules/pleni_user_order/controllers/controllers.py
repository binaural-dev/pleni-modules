# -*- coding: utf-8 -*-
# from odoo import http


# class PleniUserOrder(http.Controller):
#     @http.route('/pleni_user_order/pleni_user_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pleni_user_order/pleni_user_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pleni_user_order.listing', {
#             'root': '/pleni_user_order/pleni_user_order',
#             'objects': http.request.env['pleni_user_order.pleni_user_order'].search([]),
#         })

#     @http.route('/pleni_user_order/pleni_user_order/objects/<model("pleni_user_order.pleni_user_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pleni_user_order.object', {
#             'object': obj
#         })
