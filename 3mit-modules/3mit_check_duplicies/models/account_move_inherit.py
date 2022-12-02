# -*- coding: utf-8 -*-

from odoo import models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'


    def copy(self, default=None):
        res = super(AccountMoveInherit, self).copy(default)
        res.nro_ctrl = False
        res.supplier_invoice_number = False
        res.status = 'no_pro'
        res.islr_wh_doc_id = False

        return res
