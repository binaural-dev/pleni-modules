from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # new_currency_bs_rate = fields.Float(string='Nueva tasa de Bs', default=0.00, readonly=False)
    # active_currency_bs_rate = fields.Boolean(default=False)
    #
    # @api.onchange('new_currency_bs_rate')
    # def changeNewCurrencyBsRate(self):
    #     self.write({
    #         'new_currency_bs_rate': self.new_currency_bs_rate,
    #         'currency_bs_rate': self.new_currency_bs_rate
    #     })
    #
    # @api.onchange('pricelist_id', 'company_id')
    # def onchange_currency_id(self):
    #     if self.pricelist_id:
    #         if self.pricelist_id.currency_id != self.company_id.currency_id:
    #             self.active_currency_bs_rate = True
    #         else:
    #             self.active_currency_bs_rate = False
    #     else:
    #         self.active_currency_bs_rate = False