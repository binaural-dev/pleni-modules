odoo.define('3mit_website_button_empty_car.website_empty_mini_cart', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    const core = require('web.core');
    var publicWidget = require('web.public.widget');
    var wSaleUtils = require('website_sale.utils');
    var ThemeLazeBase = ('theme_laze.cart');

    publicWidget.registry.AtharvaCart.include({
        selector: '#wrapwrap',
        events: {
            'click #empty_mini_cart': '_onClickButtonMiniCart',
        },
        /**
         * @private
         */
         _onClickButtonMiniCart: async function(){
            let websiteOrder = $('input[name="website_sale_order"]').val();
            let resp = await ajax.rpc('/deleteOrderLines',{
                website_sale_order: websiteOrder
            });
            if(resp){
                window.location.href = '/shop?'
            }
         },
    });

    core.action_registry.add('3mit_website_button_empty_car.website_empty_mini_cart', publicWidget);

    return publicWidget;
});
