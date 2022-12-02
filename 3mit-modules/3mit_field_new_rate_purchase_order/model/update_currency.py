from odoo import models
from odoo.exceptions import UserError


class UpdateCurrency(models.Model):
    _inherit = 'purchase.order'

    def action_view_invoice(self, invoices=None):
        order = [x for x in self if x.fixed_rate_boolean]

        if order and len(order) == 1:
            new_tasa = order[0].new_currency_bs_rate
            if invoices:
                for invoice in invoices:
                    invoice.currency_bs_rate = new_tasa
        elif order and len(order) > 1:
            raise UserError('Hay mas de orden seleccionada con tasa fija.')
        else:
            new_tasa = self.env['res.currency.rate'].search([('currency_id','=',
                                                                self.env['res.currency'].search([('name', '=', 'USD')], limit=1)[0].id
                                                             )], order='name DESC', limit=1).rate_divided
            if invoices:
                for invoice in invoices:
                    invoice.currency_bs_rate = new_tasa
        res = super(UpdateCurrency, self).action_view_invoice(invoices)
        return res