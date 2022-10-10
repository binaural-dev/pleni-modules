# -*- coding: utf-8 -*-
from odoo import models, fields


class UrbanizationArea(models.Model):
    _name = 'urbanization.area'
    _description = 'Model to save urbanization/area information.'
    _rec_name = 'urbanization_name'

    urbanization_name = fields.Char(string='Urbanization name')
