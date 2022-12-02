# -*- coding: utf-8 -*-

from odoo import models, fields


class JournalBook(models.Model):
    _inherit = 'account.move.line'

    name_account_id = fields.Char(string="Descripción", related="account_id.name")
    code_account_id = fields.Char(string="Código", related="account_id.code")
