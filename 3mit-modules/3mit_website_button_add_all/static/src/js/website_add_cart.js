odoo.define('3mit_website_button_add_all.website_add_cart', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    const core = require('web.core');
    var publicWidget = require('web.public.widget');
    var wSaleUtils = require('website_sale.utils');

    publicWidget.registry.WebsiteAddCart = publicWidget.Widget.extend({
        selector: '.grid-container',
        events: {
            'click #add_cart': '_onClickButtonCart',
        },
        /**
         * @private
         */
         _onClickButtonCart: async function(){

            let arrayIds = [];
            $('#o_comparelist_table > tbody > tr').each(function() {
                if (!$(this).attr("style")) {
                    arrayIds.push($(this).attr("data-wish-id"))
                }
            });

            let resp = await ajax.rpc('/addOrderLines',{
                website_wishlist_product: arrayIds.toString()
            });
            if(resp){
                window.location.href = '/shop/cart?'
            }
         },
    });

    core.action_registry.add('3mit_website_button_add_all.website_add_cart', publicWidget);

    return publicWidget;
});
