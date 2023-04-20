odoo.define('pleni_shop.custom_onChangeUomSelection', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    const ajax = require('web.ajax');
    const core = require('web.core');
    const VariantMixin = require('sale.VariantMixin');
    var NewWebsiteSale = new publicWidget.registry.WebsiteSale();

    publicWidget.registry.WebsiteSale.include({
        events: _.extend({}, VariantMixin.events || {}, {
            'change .cart_type_select': '_onChangeUomSelection',
            'click #empty_cart': '_onClickButtonCart',
            'click #repeat_previous_cart': '_onClickButtonRepeatPreviousCart',
            'click .repeat_this_cart': '_onClickButtonRepeatThisCart',
        }),
        start: function() {
            self = this;
            self._getIsNewClient();
        },
        _getIsNewClient: async function(ev) {
            let isNewClient = await ajax.rpc('/getIsNewClient');
            if (isNewClient){
                $.each($('#repeat_previous_cart'), function (index, item) {
                    $(item).css('display', 'none')
                });
            }
        },
        /**
        * @private
        */
        _onChangeUomSelection: async function (event) {
            
            let uomIdData = $(event.currentTarget).find("option:selected").data("uom_id");
            let lineIdData = null;
            let productIdData = null;
            let selectedUomId = event.target
            for (let item of selectedUomId) {
                if (item.getAttribute('data-uom_id') === String(uomIdData)) {
                    lineIdData = item.getAttribute('line-id-value');
                    productIdData = item.getAttribute('product-id-value');
                }
            }
            let websiteOrder = $('input[name="website_sale_order"]').val();
            await ajax.rpc('/updateOrderLines', {
                'website_sale_order': websiteOrder,
                'line_data': lineIdData,
                'actual_uom_id': uomIdData,
                'product_id': productIdData,

            });

            let quantity =  $(event.target).closest('tr').find('input')
            event.currentTarget = $(quantity);

            var $input = $(quantity);
            var value = parseInt($input.val());
            if (!isNaN(value) && value >=0) {
                var cartUpdate = new publicWidget.registry.AtharvaCart();
                cartUpdate._onChangeQty(event);
            }
        },

        _onClickButtonCart: async function(){
            let websiteOrder = $('input[name="website_sale_order"]').val();
            let resp = await ajax.rpc('/deleteOrderLines',{
                website_sale_order: websiteOrder
            });
            if(resp){
                window.location.href = '/shop?'
            }
         },
         _onClickButtonRepeatPreviousCart: async function(){
            let resp = await ajax.rpc('/repeat_previous_cart');
            if(resp){
                window.location.href = '/shop/cart'
            }
        },
        _onClickButtonRepeatThisCart: async function(event){
            const sale_order_id = $(event.currentTarget).data("sale_order_id")
            let resp = await ajax.rpc('/repeat_this_cart',{
                sale_order_id: sale_order_id
            });
            if(resp){
                window.location.href = '/shop/cart'
            }
        },
    });

});