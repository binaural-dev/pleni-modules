# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError



class Costocalculo(models.Model):
    _inherit = "stock.valuation.layer"

    @api.model_create_multi
    def create(self, values):
        if values:
            for val in values:
                if val.get('stock_move_id') and not 'stock_landed_cost_id' in val:
                    stock_move = self.env['stock.move'].search([('id', '=', val['stock_move_id'])])
                    if stock_move.purchase_line_id.order_id.fixed_rate_boolean and stock_move.purchase_line_id.currency_id.name == 'USD':  #CASO COMPRA USD

                        val['unit_cost'] = (stock_move.purchase_line_id.price_unit * stock_move.purchase_line_id.order_id.fixed_rate)
                        val['value'] = val['unit_cost'] * val['quantity']
                        val['remaining_value'] = val['value']
        res = super(Costocalculo, self).create(values)
        for r in res:
            if r.product_id.quantity_svl and not r.stock_landed_cost_id:
                r.product_id.sudo().with_context(disable_auto_svl=True).write({'standard_price': r.product_id.value_svl / r.product_id.quantity_svl})
        return res

class inheritQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def create(self, vals):
        res = super(inheritQuant, self).create(vals)
        return res