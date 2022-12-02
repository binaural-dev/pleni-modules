# -*- coding: utf-8 -*-
from odoo import models, api
from datetime import timedelta


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountMoveInherit, self).create(vals_list)
        for r in res:
            if r.invoice_origin:
                sale_order_date = self.env['sale.order'].search([('name', 'ilike', r.invoice_origin)]).date_order
                if sale_order_date:
                    real_date = sale_order_date - timedelta(hours=4)
                    r.invoice_date = real_date.date()
        return res
