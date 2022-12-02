odoo.define('3mit_uom_fixing_ecommerce.custom_onChangeQuantity', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    const core = require('web.core');
    require('website_sale.website_sale');

    publicWidget.registry.WebsiteSale.include({
        /**
        * @override
        */
		_onChangeAddQuantity: async function (ev) {
			this.onChangeAddQuantity(ev);
			var add_button = $('#add_to_cart')
			var qty = $('input[name="add_qty"]').val();
			var product_id = $('input[name="product_id"]').val()
			var product_template_id = $('input[name="product_template_id"]').val()
			var pricelist_id = $('input[name="pricelist"]').val()

			const display_price = await this._rpc({
				route: '/getDisplayPrice',
				params: {
					'add_qty': qty,
					'product_id': product_id,
					'product_template_id': product_template_id,
					'pricelist_id': pricelist_id
				},
			})

			var newhtml = `<i class="fa fa-shopping-cart"></i> Agregar $${display_price.toFixed(2)}`

			add_button.html(newhtml)
        },
    });

    core.action_registry.add('3mit_uom_fixing_ecommerce.custom_onChangeQuantity', publicWidget);

    return publicWidget;

});
