# coding: utf-8

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, Warning, ValidationError

class AccountJournal(models.Model):
	_inherit = 'account.journal'

	message = fields.Html('Message')