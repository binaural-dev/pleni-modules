from odoo import models, fields, api

class PurcharseOrderCustom(models.Model):
    _inherit = 'purchase.order'

    fixed_rate = fields.Float(string='Nueva tasa de Bs', track_visibility='onchange', copy=False)

    @api.onchange('fixed_rate_boolean', 'fixed_rate')
    def onchangefixed(self):
        for s in self:
            if s.fixed_rate_boolean:
                s.new_currency_bs_rate = s.fixed_rate
            else:
                currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
                s.new_currency_bs_rate = self.env['res.currency.rate'].search(
                    [('currency_id', '=', currency_id.id), ('name', "<=", self.date_order.date())],
                    order='name desc', limit=1).rate_divided

