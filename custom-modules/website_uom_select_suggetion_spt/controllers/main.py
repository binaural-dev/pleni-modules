from asyncio.log import logger
import json

from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.variant import VariantController
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_product_configurator.controllers.main import WebsiteSale as WebsiteSaleConfigurator

import logging
_logger = logging.getLogger(__name__)


class KitsWebsiteSale(WebsiteSale):
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['GET', 'POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        """This route is called when adding a product to cart (no options)."""
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)

        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(
                kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(
                kw.get('no_variant_attribute_values'))

        product = request.env['product.product'].search(
            [('id', '=', product_id)])

        uom_id = kw.get('uom_id')
        uom = False
        try:
            if uom_id == 'NaN':
                uom = product.uom_id.id
            else:
                uom = int(uom_id)
        except:
            uom = product.uom_id.id

        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            # uom_id=int(kw.get('uom_id')) if kw.get('uom_id') else product.uom_id.id,
            uom_id=uom,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")

        if kw.get('action') and kw.get('action') == 'add_product_from_quick_view':
            return request.redirect(kw.get('path'))

        return request.redirect("/shop/cart")

    @http.route(['/sale-order'], type='json', auth="public", website=True, method=['post'])
    def getSaleOrder(self, **post):
        """This route is called when displaying the message about stock. i.e. remaning product in stock,
        quantity of selected product added in cart.
        """
        # self.ensure_one()
        order = request.website.sale_get_order()
        order_line = order.order_line
        prod_uom = False
        ordered_qty = False
        prod = post['product_id']
        prod_uom = post['uom_name']
        selected_products = order_line.filtered(
            lambda l: l.product_id.id == prod)
        # selected_uom = selected_products.filtered(lambda l: l.product_uom.name == prod_uom )
        if order_line:
            if len(order.order_line) > 1:
                # if selected_products:
                selected_uom = selected_products.filtered(
                    lambda l: l.product_uom.name == prod_uom)
                prod_uom = selected_uom.product_uom.name
                ordered_qty = selected_uom.product_uom_qty

            else:
                prod_uom = order_line.product_uom.name
                ordered_qty = order_line.product_uom_qty
        # prod_id = post['sale_order']
        # if order:
        #     if len(order_line)
            val = {
                'sale_order': order,
                'uom': prod_uom,
                'qty': ordered_qty,
                # 'sale_order_line' : order_line,
            }
        else:
            val = {
                'uom': post.get('uom_name'),
                'qty': post.get('cart_qty'),
            }

        return val


class KitsWebsiteSaleConfigurator(WebsiteSaleConfigurator):
    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'], website=True, multilang=False)
    def cart_options_update_json(self, product_and_options, goto_shop=None, lang=None, **kwargs):
        """This route is called when submitting the optional product modal.
            The product without parent is the main product, the other are options.
            Options need to be linked to their parents with a unique ID.
            The main product is the first product in the list and the options
            need to be right after their parent.
            product_and_options {
                'product_id',
                'product_template_id',
                'quantity',
                'parent_unique_id',
                'unique_id',
                'product_custom_attribute_values',
                'no_variant_attribute_values'
            }
        """
        if lang:
            request.website = request.website.with_context(lang=lang)

        order = request.website.sale_get_order(force_create=True)
        if order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order(force_create=True)

        product_and_options = json.loads(product_and_options)
        if product_and_options:
            # The main product is the first, optional products are the rest
            main_product = product_and_options[0]
            value = order._cart_update(
                product_id=main_product['product_id'],
                add_qty=main_product['quantity'],
                uom_id=kwargs.get("uom_id"),
                product_custom_attribute_values=main_product['product_custom_attribute_values'],
                no_variant_attribute_values=main_product['no_variant_attribute_values'],
            )

            # Link option with its parent.
            option_parent = {main_product['unique_id']: value['line_id']}
            for option in product_and_options[1:]:
                parent_unique_id = option['parent_unique_id']
                option_value = order._cart_update(
                    product_id=option['product_id'],
                    set_qty=option['quantity'],
                    linked_line_id=option_parent[parent_unique_id],
                    product_custom_attribute_values=option['product_custom_attribute_values'],
                    no_variant_attribute_values=option['no_variant_attribute_values'],
                )
                option_parent[option['unique_id']] = option_value['line_id']

        return str(order.cart_quantity)


class KitsVariantController(VariantController):
    @http.route()
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        res = super(KitsVariantController, self).get_combination_info(
            product_template_id, product_id, combination, add_qty, pricelist_id, **kw)
        uom = request.env['uom.uom'].sudo().browse(kw.get('uom_id'))
        product = request.env['product.product'].sudo().browse(product_id)
        self._update_combination_vals(request, res, uom, add_qty, pricelist_id)
        if res.get('virtual_available') and product.uom_id.id != uom.id:
            # virtual_available = int(product.uom_id._compute_quantity(res.get('virtual_available'), uom))
            now_in_stock = product.qty_available
            virtual_available = int(
                product.uom_id._compute_quantity(now_in_stock, uom))
            res.update({
                'virtual_available': virtual_available,
                'virtual_available_formatted': request.env['ir.qweb.field.float'].value_to_html(virtual_available, {'decimal_precision': 'Product Unit of Measure'}),
            })

        return res

    # Reescritura de las reglas para los descuentos online
    def _update_combination_vals(self, request, vals, uom, add_qty, pricelist_id):
        pricelist_items = request.env['product.pricelist.item'].sudo().search([('pricelist_id', '=', pricelist_id.id), '|', (
            'product_tmpl_id', '=', vals['product_template_id']), ('product_id', '=', vals['product_id'])], order='min_quantity asc')
        base_oum = request.env['uom.uom'].sudo().search(
            [('category_id', '=', uom.category_id.id), ('uom_type', '=', 'reference')])
        real_qty = add_qty / uom.factor if uom.uom_type == 'bigger' else add_qty * uom.factor
        price = vals.get('list_price')
        show_discount = False
        for item in pricelist_items:
            if real_qty >= item.min_quantity:
                #price = item.fixed_price
                if uom.factor != 0:
                    if 1 < item.min_quantity <= 1 / uom.factor:
                        show_discount = True
                        price = item.fixed_price

        if len(pricelist_items):
            real_list_price = max(
                [item.fixed_price for item in pricelist_items])
        else:
            real_list_price = 0

        vals.update({
            'price': price,  # precio a facturar
            'list_price': real_list_price,  # precio a tachar
            'uom_id_name': uom.name,
            'has_discounted_price': price < real_list_price,
            'uom_name': base_oum.name,
            'show_discount': show_discount
        })
        # _logger.info(vals)
        return vals
