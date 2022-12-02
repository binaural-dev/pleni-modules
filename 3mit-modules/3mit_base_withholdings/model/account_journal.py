# coding: utf-8
###########################################################################
import time
from odoo import api, fields, models, exceptions
from odoo.fields import _

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    default_iva_account = fields.Many2one('account.account', string='Cuenta retención IVA', groups="3mit_grupo_localizacion.group_localizacion")
    default_islr_account = fields.Many2one('account.account', string='Cuenta retención ISLR', groups="3mit_grupo_localizacion.group_localizacion")
    is_iva_journal = fields.Boolean(default=False, groups="3mit_grupo_localizacion.group_localizacion")
    is_islr_journal = fields.Boolean(default=False, groups="3mit_grupo_localizacion.group_localizacion")



