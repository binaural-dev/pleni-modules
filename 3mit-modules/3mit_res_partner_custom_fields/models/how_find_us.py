# -*- coding: utf-8 -*-
from odoo import models, fields


class HowFindUs(models.Model):
    _name = 'find.us'
    _description = 'Model to save how to find us information.'
    _rec_name = 'type_name'

    type_name = fields.Char(string='Name')
