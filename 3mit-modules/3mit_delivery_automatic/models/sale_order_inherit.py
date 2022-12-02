# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import models, fields, api, _
from functools import partial
from odoo.tools.misc import formatLang


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(SaleOrderInherit, self).write(vals)
        for r in self:
            if 'carrier_id' not in vals:
                r.changing_order_line()
            amount_tax_usd, amount_untaxed_usd = 0, 0
            for so_line in self.order_line:
                so_line._onchange_price()
                amount_aux = (so_line.price_unit_usd * so_line.product_uom_qty)
                amount_untaxed_usd += (so_line.price_unit_usd * so_line.product_uom_qty)
                if so_line.tax_id:
                    amount_tax_usd += ((so_line.tax_id.amount / 100) * amount_aux)

            query_update = f"""UPDATE sale_order SET amount_tax_usd = {amount_tax_usd}, amount_untaxed_usd = {amount_untaxed_usd}, amount_total_usd = {amount_tax_usd + amount_untaxed_usd} WHERE id = {r.id}"""
            self.env.cr.execute(query_update)
        return res

    @api.onchange('order_line')
    def changing_order_line(self):
        if len(self.order_line) > 0:
            amount_real = sum([line.price_total for line in self.order_line if not line.is_delivery])
            if amount_real > 50:
                delivery_line = self.env['sale.order.line'].search([('order_id', '=', self.id), ('is_delivery', '=', True)])
                if not delivery_line:
                    return
                delivery_line.price_total = 0.0
            else:
                id_2_search = False
                if len(self.ids) > 0:
                    id_2_search = self.ids[0]
                if id_2_search:
                    delivery_line_exists = self.env['sale.order.line'].search([('is_delivery', '=', True), ('order_id', '=', id_2_search)])
                    if not delivery_line_exists:
                        delivery_carrier = self.env['delivery.carrier'].search([('name', '=ilike', 'Delivery')], order='write_date desc', limit=1)
                        if not delivery_carrier:
                            delivery_carrier = delivery_carrier.create({
                                'name': 'Delivery',
                                'product_id': self.env['product.product'].search([('name', '=ilike', 'Delivery'), ('type', '=', 'service')]).id,
                                'fixed_price': 3
                            })
                        self._create_delivery_line(delivery_carrier, delivery_carrier.fixed_price)

    def _create_delivery_line(self, carrier, price_unit):
        SaleOrderLine = self.env['sale.order.line']
        if self.partner_id:
            # set delivery detail in the customer language
            carrier = carrier.with_context(lang=self.partner_id.lang)

        # Apply fiscal position
        taxes = carrier.product_id.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        taxes_ids = taxes.ids
        if self.partner_id and self.fiscal_position_id:
            taxes_ids = self.fiscal_position_id.map_tax(taxes, carrier.product_id, self.partner_id).ids

        # Create the sales order line
        carrier_with_partner_lang = carrier.with_context(lang=self.partner_id.lang)
        if carrier_with_partner_lang.product_id.description_sale:
            so_description = '%s: %s' % (carrier_with_partner_lang.name, carrier_with_partner_lang.product_id.description_sale)
        else:
            so_description = carrier_with_partner_lang.name
        values = {
            'order_id': self.ids[0],
            'name': so_description,
            'product_uom_qty': 1,
            'product_uom': carrier.product_id.uom_id.id,
            'product_id': carrier.product_id.id,
            'tax_id': [(6, 0, taxes_ids)],
            'is_delivery': True,
        }
        if carrier.invoice_policy == 'real':
            values['price_unit'] = 0
            values['name'] += _(' (Estimated Cost: %s )', self._format_currency_amount(price_unit))
        else:
            values['price_unit'] = price_unit
        if carrier.free_over and self.currency_id.is_zero(price_unit):
            values['name'] += '\n' + 'Free Shipping'
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        sol = SaleOrderLine.sudo().create(values)

        # probando solucionar el bug #13
        self.delivery_set = True

        return sol


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _onchange_price_sql(self):
        vals = {}
        if self.order_id.pricelist_id:
            if self.order_id.pricelist_id.currency_id.id == 3:
                vals = {
                    'price_unit_usd': self.price_unit,
                    'price_subtotal_usd': self.price_subtotal
                }
            elif self.order_id.pricelist_id.currency_id.id != 3:
                vals = {
                    'price_unit_usd': self.order_id.pricelist_id.currency_id._convert(self.price_unit, self.env.company.currency_id, self.env.company, self.order_id.date_order, False),
                    'price_subtotal_usd': self.order_id.pricelist_id.currency_id._convert(self.price_subtotal, self.env.company.currency_id, self.env.company, self.order_id.date_order, False)
                }
        return vals
