# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.warehouse_id = False

    @api.onchange('user_id')
    def onchange_user_id(self):
        super().onchange_user_id()
        self.warehouse_id = False
