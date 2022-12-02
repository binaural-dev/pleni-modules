# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrderInherit, self).create(vals_list)
        for r in res:
            if r.website_id or 'Sitio web' in r.team_id.name or 'Website' in r.team_id.name:
                r.journal_id = r.transaction_ids.acquirer_id.journal_id.ids
        return res
    
    def write(self, vals):
        if not self.team_id:
            return super(SaleOrderInherit, self).write(vals)
        if (self.website_id or 'Sitio web' in self.team_id.name or 'Website' in self.team_id.name) and not self.journal_id:
            vals['journal_id'] = [[6, 0,  self.transaction_ids.acquirer_id.journal_id.ids]]
        return super(SaleOrderInherit, self).write(vals)

    journal_id = fields.Many2many('account.journal', string='Método de pago', domain='[("type","in",("bank", "cash"))]')
