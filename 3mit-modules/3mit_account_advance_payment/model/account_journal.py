# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountJournalInheritNewAccount(models.Model):
    _inherit = 'account.journal'

    extra2_account_id = fields.Many2one('account.account', string="cuenta extra 2")

