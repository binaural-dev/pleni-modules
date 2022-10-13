odoo.define('website_uom_select_suggetion.warning_msg', function (require) {
    'use strict';

    var VariantMixin = require('sale.VariantMixin');
    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var QWeb = core.qweb;
    var xml_load = ajax.loadXML(
        '/website_uom_select_suggetion_spt/static/src/components/warning_msg.xml',
        QWeb
    );

    /**
     * Addition to the variant_mixin._onChangeCombination
     *
     * This will prevent the user from selecting a quantity that is not available in the
     * stock for that product.
     *
     * It will also display various info/warning messages regarding the select product's stock.
     *
     * This behavior is only applied for the web shop (and not on the SO form)
     * and only for the main product.
     *
     * @param {MouseEvent} ev
     * @param {$.Element} $parent
     * @param {Array} combination
     */
    VariantMixin._onChangeCombinationStock = function (ev, $parent, combination) {
        debugger;
        var product_id = 0;
        // needed for list view of variants
        if ($parent.find('input.product_id:checked').length) {
            product_id = $parent.find('input.product_id:checked').val();
        } else {
            product_id = $parent.find('.product_id').val();
        }
        var isMainProduct = combination.product_id &&
            ($parent.is('.js_main_product') || $parent.is('.main_product')) &&
            combination.product_id === parseInt(product_id);

        if (!this.isWebsite || !isMainProduct) {
            return;
        }

        // ajax.jsonRpc('/sale-order','call', combination)
        //     .then(function(val){
        //         debugger
                
        //         var order = val['sale_order']
        //         combination['sale_order'] = order;
        //     }) 
        
        var qty = $parent.find('input[name="add_qty"]').val();

        $parent.find('#add_to_cart').removeClass('out_of_stock');
        $parent.find('#buy_now').removeClass('out_of_stock');
        if (combination.product_type === 'product' && _.contains(['always', 'threshold'], combination.inventory_availability)) {
            combination.virtual_available -= parseInt(combination.cart_qty);
            if (combination.virtual_available < 0) {
                combination.virtual_available = 0;
            }
            // Handle case when manually write in input
            if (qty > combination.virtual_available) {
                var $input_add_qty = $parent.find('input[name="add_qty"]');
                qty = combination.virtual_available || 1;
                $input_add_qty.val(qty);
            }
            if (qty > combination.virtual_available
                || combination.virtual_available < 1 || qty < 1) {
                $parent.find('#add_to_cart').addClass('disabled out_of_stock');
                $parent.find('#buy_now').addClass('disabled out_of_stock');
            }
        }

        ajax.jsonRpc('/sale-order','call', combination)
        .then(function(val){
            debugger
            
            var uom = val['uom']
            var qty = val['qty']
            combination['selected_uom'] = uom;
            combination['ordered_qty']= qty

            xml_load.then(function () {
                debugger;
            
                $('.oe_website_sale')
                    .find('.availability_message_' + combination.product_template)
                    .remove();
    
                var $message = $(QWeb.render(
                    'website_uom_select_suggetion_spt.product_availability_',
                    combination
                ));
                $('div.availability_messages').html($message);
            });

        })   
        
        // xml_load.then(function () {
            
        //     $('.oe_website_sale')
        //         .find('.availability_message_' + combination.product_template)
        //         .remove();

        //     var $message = $(QWeb.render(
        //         'website_uom_select_suggetion_spt.product_availability_',
        //         combination
        //     ));
        //     $('div.availability_messages').html($message);
        // });
        ev.preventDefault();
        // var productID = combination.product_id
        // this._rpc({
        //     model: 'sale.order',
        //     method: 'warning_msg',
        //     args: [productID],
        // })
        // .then(function(val){

        //     qty = val['cart_qty']
        //     uom = val['uom']
        //    var ordered_qty =  qty ;
        //    var uom = uom;
        //    var msg = "you have already ordered "+ ordered_qty + " "+ uom + ' ' + "in your cart";
        //     $('div.availability_messages').html(msg);

        // });
    };
});