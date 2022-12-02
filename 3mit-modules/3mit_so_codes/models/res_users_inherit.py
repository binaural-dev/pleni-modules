# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    so_code = fields.Char('Código de orden')
    so_sequence_code = fields.Integer('Próximo número de secuencia')
    so_sequence_length = fields.Integer('Tamaño de la secuencia')
