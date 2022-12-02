# coding: utf-8
from asyncio.log import logger
from odoo import models, fields, api


class SaleOrderInheritCompute(models.Model):
    _inherit = 'sale.order.line'

    price_unit_usd = fields.Float('Precio unitario Bs', digits=(12, 2))
    price_subtotal_usd = fields.Float('Precio Subtotal Bs', digits=(12, 2))
    tax_usd = fields.Float('Impuestos', digits=(12, 2))
    order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True,
                               copy=False)
    rate_search = fields.Float('Tasa Busqueda')
    amount_untaxed_usd = fields.Float('Base Imponible $', digits=(12, 2))
    amount_tax_usd = fields.Float('Impuesto $', digits=(12, 2))
    amount_total_usd = fields.Float('Total $', digits=(12, 2))

    @api.onchange('order_id', 'product_id', 'product_uom_qty', 'price_unit', 'tax_id', 'name')
    def _onchange_price(self):
        if self.order_id.pricelist_id and self.loc_ven:
            if self.order_id.pricelist_id.currency_id.id == 3:
                self.price_unit_usd = self.price_unit
                self.price_subtotal_usd = self.price_subtotal
            else:
                if self.order_id.pricelist_id.currency_id.id != 3:
                    self.price_unit_usd = self.order_id.pricelist_id.currency_id._convert(
                        self.price_unit, self.env.company.currency_id, self.env.company, self.order_id.date_order, False)
                    self.price_subtotal_usd = self.order_id.pricelist_id.currency_id._convert(
                        self.price_subtotal, self.env.company.currency_id, self.env.company, self.order_id.date_order, False)


class SaleOrderInheritComputeTwo(models.Model):
    _inherit = 'sale.order'

    price_unit_usd = fields.Float('Precio unitario $', digits=(12, 2))
    price_subtotal_usd = fields.Float('Precio Subtotal $', digits=(12, 2))
    tax_usd = fields.Float('Impuestos', digits=(12, 2))
    rate_search = fields.Float('Tasa buqueda')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True, readonly=True, states={'draft': [('readonly', False)]},
                                  track_visibility='always')
    amount_untaxed_usd = fields.Float(
        'Base Imponible Bs', digits=(12, 2), store=True, readonly=True)
    amount_tax_usd = fields.Float(
        'Impuesto Bs', digits=(12, 2), store=True, readonly=True)
    amount_total_usd = fields.Float(
        'Total Bs', digits=(12, 2), store=True, readonly=True)
    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines',
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
                                 auto_join=True)

    @api.onchange('pricelist_id', 'order_line', 'amount_untaxed', 'amount_total', 'amount_tax')
    def _onchange_amount_total(self):

        if self.amount_untaxed > 0 and self.amount_total > 0 and self.loc_ven:
            fecha_order = self.date_order
            if self.pricelist_id.currency_id.id != 3:
                self.amount_untaxed_usd = self.pricelist_id.currency_id._convert(
                    self.amount_untaxed, self.env.company.currency_id, self.env.company, self.date_order, False)
                acumulado = 0
                for i in self.amount_by_group:
                    tasa = 0
                    if i[2] != 0:
                        tasa = round(i[1] / i[2], 2)
                    value = self.pricelist_id.currency_id._convert(
                        i[2], self.env.company.currency_id, self.env.company, self.date_order, False)
                    acumulado = acumulado + value * tasa
                self.amount_tax_usd = acumulado
                self.amount_total_usd = self.amount_untaxed_usd + self.amount_tax_usd
            for i in self.order_line:
                if i.price_unit_usd == 0:
                    i._onchange_price()

    def update_prices(self):
        super(SaleOrderInheritComputeTwo, self).update_prices()
        for i in self:
            for j in i.order_line:
                j._onchange_price()
            i._onchange_amount_total()

    def copy(self, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default.update({
            'currency_id': self.currency_id.id
        })
        return super(SaleOrderInheritComputeTwo, self).copy(default)
