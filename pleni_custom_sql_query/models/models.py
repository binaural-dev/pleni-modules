# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class pleni_custom_sql_query(models.Model):
#     _name = 'pleni_custom_sql_query.pleni_custom_sql_query'
#     _description = 'pleni_custom_sql_query.pleni_custom_sql_query'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
