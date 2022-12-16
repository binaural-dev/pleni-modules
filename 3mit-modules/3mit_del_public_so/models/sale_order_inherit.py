# -*- coding: utf-8 -*-
from odoo import models
from datetime import timedelta, datetime


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def check_public_user_budgets(self):
        query_search = f"""SELECT id FROM res_partner WHERE id = 4 OR name LIKE '%Public user%' AND type = 'contact'"""
        self.env.cr.execute(query_search)
        res = self.env.cr.dictfetchone()
        create_date_plus_one_day = datetime.now() - timedelta(days=1, hours=4)
        public_user_budgets = self.env['sale.order'].search([('state', '=', 'draft'), ('partner_id', '=', res.get('id')), ('create_date', '<=', create_date_plus_one_day)])
        for budget in public_user_budgets:
            budget.unlink()
