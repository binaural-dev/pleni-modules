# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class DeleteOrderLines(http.Controller):
    @http.route('/deleteOrderLines', auth='none', type='json', cors='*')
    def delete_order_lines(self, website_sale_order, **kwarg):
        if not website_sale_order: return False
        order = request.env['sale.order'].sudo().browse(int(website_sale_order))
        for element in order.order_line:
            element.unlink()
        return True


class UpdateOrderLines(http.Controller):
    @http.route('/updateOrderLines', auth='none', type='json', cors='*')
    def update_order_lines(self, **kwarg):
        if not kwarg.get('website_sale_order'): return False
        order = request.env['sale.order'].sudo().search([('id', '=', kwarg.get('website_sale_order'))])
        uom_id = request.env['uom.uom'].sudo().search([('id', '=', kwarg.get('actual_uom_id'))])
        product_id = request.env['product.product'].sudo().search([('id', '=', kwarg.get('product_id'))])
        line_order = request.env['sale.order.line'].sudo().search([('id', '=', kwarg.get('line_data'))])
        product_uom_qty = line_order.product_uom_qty

        line_order.write({
            'product_uom': kwarg.get('actual_uom_id'),
        })
        # if line_order in order.order_line:
        #     line_order.unlink()
        # line = request.env['sale.order.line'].sudo().create({
        #     'order_id': order.id,
        #     'product_id': product_id.id,
        #     'product_uom': uom_id.id,
        #     'product_uom_qty': product_uom_qty
        # })
        return line_order


class GetSaleOrderLine(http.Controller):
    @http.route('/getSaleOrderLine', auth='none', type='json', cors='*')
    def get_sale_order_line(self, **kwarg):
        line_order = request.env['sale.order.line'].sudo().search([('id', '=', kwarg.get('line_data'))])
        return {line_order.price_unit}
