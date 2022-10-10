# -*- coding: utf-8 -*-
# from odoo import http


# class 3mitIgtfWithholding(http.Controller):
#     @http.route('/3mit_igtf_withholding/3mit_igtf_withholding/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/3mit_igtf_withholding/3mit_igtf_withholding/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('3mit_igtf_withholding.listing', {
#             'root': '/3mit_igtf_withholding/3mit_igtf_withholding',
#             'objects': http.request.env['3mit_igtf_withholding.3mit_igtf_withholding'].search([]),
#         })

#     @http.route('/3mit_igtf_withholding/3mit_igtf_withholding/objects/<model("3mit_igtf_withholding.3mit_igtf_withholding"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('3mit_igtf_withholding.object', {
#             'object': obj
#         })
