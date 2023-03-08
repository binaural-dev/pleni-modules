from asyncio.log import logger
from odoo import models, fields, api, _
from odoo.addons.website.models import ir_http


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_uom_category_id = fields.Many2one('uom.category',
                                              string="Categorías de presentaciones de venta",
                                              compute="_get_uom_category")

    product_uom_ids = fields.Many2many('uom.uom', 'product_template_uom_rel',
                                       'product_id', 'uom_id',
                                       string="Presentaciones de venta")

    @api.depends('uom_id')
    def _get_uom_category(self):
        for rec in self:
            rec.product_uom_category_id = rec.uom_id.category_id.id
            # rec.product_uom_ids = [(4,rec.uom_id.id)]

    def _get_combination_info_display(self, line,  pricelist=None):
        product_id = self.env['product.product'].search(
            [('product_tmpl_id', '=', self.id)])
        price_list_items = self.env['product.pricelist.item'].search([('pricelist_id', '=', pricelist.id), '|', (
            'product_tmpl_id', '=', self.id), ('product_id', '=', product_id.id)], order='min_quantity asc')
        real_price = discounted_price = round(
            self.list_price * 1, 2)
        real_qty = round(line.product_uom_qty / \
            line.product_uom.factor if line.product_uom.uom_type == 'bigger' else line.product_uom_qty)
        min_price = discounted_price if discounted_price != 0 else (
            price_list_items[0].fixed_price if len(price_list_items) else 0)

        if not price_list_items:
            return {
                'has_discount': False,
                'discounted_price': min_price / line.product_uom.factor if line.product_uom.uom_type == 'bigger' else min_price,
                'real_price': real_price / line.product_uom.factor if line.product_uom.uom_type == 'bigger' else real_price
            }
        for item in price_list_items:
            if real_qty >= item.min_quantity:
                real_price = item.fixed_price

        return {
            'has_discount': real_price < min_price,
            'discounted_price': min_price / line.product_uom.factor if line.product_uom.uom_type == 'bigger' else min_price,
            'real_price': real_price / line.product_uom.factor if line.product_uom.uom_type == 'bigger' else real_price
        }


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_cart_qty(self):
        website = ir_http.get_request_website()
        if not website:
            self.cart_qty = 0
            return
        cart = website.sale_get_order()
        for product in self:
            product.cart_qty = sum(cart.order_line.filtered(
                lambda p: p.product_id.id == product.id and p.product_uom.id == product.uom_id.id).mapped('product_uom_qty')) if cart else 0
