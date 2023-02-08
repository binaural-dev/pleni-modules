# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class pleni_auth_api_key(models.Model):
#     _name = 'pleni_auth_api_key.pleni_auth_api_key'
#     _description = 'pleni_auth_api_key.pleni_auth_api_key'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
