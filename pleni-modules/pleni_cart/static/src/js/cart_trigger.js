odoo.define('pleni_cart.website_empty_cart', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    const core = require('web.core');
    var publicWidget = require('web.public.widget');

    publicWidget.registry.WebsiteEmptyCart = publicWidget.Widget.extend({
        selector: '.clearfix',
        events: {
            'click #empty_cart': '_onClickButtonCart',
        },
        /**
         * @private
         */
         _onClickButtonCart: async function(){
            let websiteOrder = $('input[name="website_sale_order"]').val();
            let resp = await ajax.rpc('/deleteOrderLines',{
                website_sale_order: websiteOrder
            });
            if(resp){
                window.location.href = '/shop?'
            }
         },
    });

    core.action_registry.add('pleni_cart.website_empty_cart', publicWidget);

    return publicWidget;
});

odoo.define('pleni_cart.website_empty_mini_cart', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    const core = require('web.core');
    var publicWidget = require('web.public.widget');

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
        }
    });

    core.action_registry.add('pleni_cart.website_empty_mini_cart', publicWidget);

    return publicWidget;
});
