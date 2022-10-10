# -*- coding: utf-8 -*-
# from odoo import http


# class 3mitMultimoneda(http.Controller):
#     @http.route('/3mit_multimoneda/3mit_multimoneda/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/3mit_multimoneda/3mit_multimoneda/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('3mit_multimoneda.listing', {
#             'root': '/3mit_multimoneda/3mit_multimoneda',
#             'objects': http.request.env['3mit_multimoneda.3mit_multimoneda'].search([]),
#         })

#     @http.route('/3mit_multimoneda/3mit_multimoneda/objects/<model("3mit_multimoneda.3mit_multimoneda"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('3mit_multimoneda.object', {
#             'object': obj
#         })
