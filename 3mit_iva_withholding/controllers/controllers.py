# -*- coding: utf-8 -*-
# from odoo import http


# class 3mitIvaWithholding(http.Controller):
#     @http.route('/3mit_iva_withholding/3mit_iva_withholding/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/3mit_iva_withholding/3mit_iva_withholding/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('3mit_iva_withholding.listing', {
#             'root': '/3mit_iva_withholding/3mit_iva_withholding',
#             'objects': http.request.env['3mit_iva_withholding.3mit_iva_withholding'].search([]),
#         })

#     @http.route('/3mit_iva_withholding/3mit_iva_withholding/objects/<model("3mit_iva_withholding.3mit_iva_withholding"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('3mit_iva_withholding.object', {
#             'object': obj
#         })
