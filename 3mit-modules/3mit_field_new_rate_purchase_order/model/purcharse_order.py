from odoo import models, fields, api

class PurcharseOrderCustom(models.Model):
    _inherit = 'purchase.order'

    new_currency_bs_rate = fields.Float(string='Nueva tasa de Bs',
                                        default=lambda self:
                                            self.env['res.currency.rate'].search([
                                                            (
                                                                'currency_id',
                                                                '=',
                                                                self.env['res.currency'].search([('name', '=', 'USD')], limit=1)[0].id
                                                             )
                                                        ], order='name DESC', limit=1).rate_divided, readonly=False)
    active_new_currency_bs_rate = fields.Boolean(default=False)
    fixed_rate_boolean = fields.Boolean(default=False, copy=False)

    @api.onchange('date_order')
    def change_rate(self):
        if self.active_new_currency_bs_rate and self.state == 'draft':
            currency_id = currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            self.new_currency_bs_rate = self.env['res.currency.rate'].search(
                [('currency_id', '=', currency_id.id), ('name', "<=", self.date_order.date())],
                order='name desc', limit=1).rate_divided


    @api.onchange('new_currency_bs_rate')
    def changeNewCurrencyBsRate(self):
        self.write({
            'new_currency_bs_rate': self.new_currency_bs_rate,
            'currency_bs_rate': self.new_currency_bs_rate
        })

    @api.onchange('company_id', 'currency_id')
    def onchange_currency_id(self):
        if self.company_id or self.currency_id:
            if self.company_id.currency_id != self.currency_id and self.currency_id.name == 'USD':
                self.active_new_currency_bs_rate = True
            else:
                self.active_new_currency_bs_rate = False
        else:
            self.active_new_currency_bs_rate = False

    def write(self, vals):
        res = super(PurcharseOrderCustom, self).write(vals)
        for i in self:
            if i.company_id.currency_id != i.currency_id and i.currency_id.name == 'USD':
                i._write({'active_new_currency_bs_rate': True})
        return res