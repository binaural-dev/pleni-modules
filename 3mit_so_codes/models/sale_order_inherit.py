# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrderInherit, self).create(vals_list)
        for r in res:
            if r.user_id.so_code and r.user_id.so_sequence_code and r.user_id.so_sequence_length:
                query_update_order = f"""UPDATE sale_order SET name = '{r.user_id.so_code}{str(r.user_id.so_sequence_code).zfill(r.user_id.so_sequence_length)}' WHERE id = {r.id}"""
                self.env.cr.execute(query_update_order)
                r.user_id.so_sequence_code += 1
        return res
