odoo.define('3mit_website_button_empty_car.website_empty_mini_cart', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    const core = require('web.core');
    var publicWidget = require('web.public.widget');
    // var wSaleUtils = require('website_sale.utils');
    // var ThemeLazeBase = ('theme_laze.cart');

    publicWidget.registry.AtharvaCart.include({
        selector: '#wrapwrap',
        events: {
            'click #empty_mini_cart': '_onClickButtonMiniCart',
            'change .m_c_info .m_c_qty #mini_cart_uom': '_onChangeMiniCartUom',
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
        _onChangeMiniCartUom: async function(event) {
            let uomIdData = $('#uom_id').find("option:selected").data("uom_id");
            let lineIdData = null
            let productIdData = null
            let selectedUomId = event.target
             for (let item of selectedUomId) {
                 if (item.getAttribute('data-uom_id') === String(uomIdData)) {
                     lineIdData = item.getAttribute('value');
                     productIdData = item.getAttribute('product-id-value');
                 }
             }

             let websiteOrder = $('input[name="website_sale_order"]').val();
             await ajax.rpc('/updateOrderLines', {
                 'website_sale_order': websiteOrder,
                 'line_data': lineIdData,
                 'actual_uom_id': uomIdData,

             });

             event.currentTarget = $('.js_quantity.form-control.quantity.p-1.text-center');
             this._onChangeQty(event);

             // let actualPriceUnit = await ajax.rpc('/getSaleOrderLine', {
             //     'line_data': lineIdData,
             // });
             //
             // let mini_cart_lines = document.getElementsByClassName('mini_cart_lines');
             // Array.from(mini_cart_lines).forEach(function (element) {
             //    if (element.getElementsByClassName('m_c_img')[0].children[0].getAttribute('data-oe-id') === productIdData) {
             //        element.getElementsByClassName('m_c_info')[0].getElementsByClassName('m_c_prod_price')[0].getElementsByClassName('product_price')[0].getElementsByClassName('oe_price_h4 css_editable_mode_hidden')[0].getElementsByClassName('oe_price')[0].innerText = `$ ${actualPriceUnit}`
             //    }
             // });

        }
    });

    core.action_registry.add('3mit_website_button_empty_car.website_empty_mini_cart', publicWidget);

    return publicWidget;
});
