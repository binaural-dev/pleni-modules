odoo.define('pleni_shop.custom_quickView', function (require) {
    'use strict';

    require("web.dom_ready");
    var QuickView = require('atharva_theme_base.product_quick_veiw')

    const publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    const core = require('web.core');

    publicWidget.registry.quick_view.include({
        /**
        * @override
        */
        _quickViewLoad:function(evt){
            var pid = $(evt.currentTarget).attr("data-product_template_id");
            ajax.jsonRpc("/get_prod_quick_view_details", "call", {"prod_id":pid}).then(function(data)
            {   
                var sale = new publicWidget.registry.WebsiteSale();
                changeAmount();
                $(".quick_cover").append(data);
                $(".quick-cover-overlay").fadeIn();
                sale.init();
                $(".quick_cover").css("display", "block");
                $("[data-attribute_exclusions]").on("change", function(event) {
                    sale.onChangeVariant(event);
                });
                $("[data-attribute_exclusions]").trigger("change");
                $(".css_attribute_color input").click(function(event){
                    sale._changeColorAttribute(event);
                });
                // Add to cart from Quick View
                $(".a-submit").on("click", async function(event) {

                    const user_not_logged = await ajax.rpc('/get_user_logged')
                    if (user_not_logged) {
                        window.location = "/web/login";
                        return;
                    }

                    event.preventDefault();
                    var def = async () => {
                        sale.isBuyNow = $(event.currentTarget).attr('id') === 'buy_now';
                        var $form = $(event.currentTarget).closest('form')
                        var self = sale;
                        sale.$form = $form;
                    
                        var productSelector = [
                            'input[type="hidden"][name="product_id"]',
                            'input[type="radio"][name="product_id"]:checked'
                        ];
                    
                        var productReady = sale.selectOrCreateProduct(
                            $form,
                            parseInt($form.find(productSelector.join(', ')).first().val(), 10),
                            $form.find('.product_template_id').val(),
                            false
                        );
                        var uom = $('#uom_id').find("option:selected").data("uom_id");
                        const factor = await ajax.rpc('/getUomFactor', {'uom_id': uom})
                        return productReady.then(function (productId) {
                            $form.find(productSelector.join(', ')).val(productId);
                        
                            self.rootProduct = {
                                product_id: productId,
                                quantity: (parseFloat($form.find('input[name="add_qty"]').val())*factor).toFixed(0) || 1,
                                uom_id: parseInt($form.find('#uom_id').find(':selected').data('uom_id')),
                                product_custom_attribute_values: self.getCustomVariantValues($form.find('.js_product')),
                                variant_values: self.getSelectedVariantValues($form.find('.js_product')),
                                no_variant_attribute_values: self.getNoVariantAttributeValues($form.find('.js_product')),
                                action: 'add_product_from_quick_view',
                                path: window.location.pathname + window.location.search
                            };
                        
                            return self._onProductReady();
                        });
                    
                    };
                    if ($('.js_add_cart_variants').children().length) {
                        return sale._getCombinationInfo(event).then(() => {
                            return !$(event.target).closest('.js_product').hasClass("css_not_available") ? def() : Promise.resolve();
                        });
                    }
                    return def();
                });
                // Add Quantity from Quick View
                $("a.js_add_cart_json").on("click", async function(event) {
                    var qty = parseFloat($('input[name="add_qty"]').val());
                    var uom = $('#uom_id').find("option:selected").data("uom_id");
                    if (!uom) return
                    const factor = await ajax.rpc('/getUomFactor', { 'uom_id': uom, })
                    var $link = $(event.currentTarget);
                    var $input = $link.closest('.input-group').find("input");
                    var min = parseFloat($input.data("min") || 0);
                    var max = parseFloat($input.data("max") || Infinity);
                    var newQuantity = ($link.has(".fa-minus").length ? -1/factor : 1/factor) + qty;
                    var newQty = newQuantity > min ? (newQuantity < max ? newQuantity : max) : min;
                    if (newQty !== qty) {
                        $('input[name="add_qty"]').val(newQty.toFixed(2)).trigger('change');
                    }
                    return false
                    // sale._onClickAddCartJSON(event);
                });
                // Change Quantity from Quick View
                $("input[name='add_qty']").on("change", async function(event) {
                    // sale._onChangeAddQuantity(event);
                    sale.onChangeAddQuantity(event);
			        var add_button = $('#add_to_cart');
			        var qty = $('input[name="add_qty"]').val();
			        var product_id = $('input[name="product_id"]').val();
			        var product_template_id = $('input[name="product_template_id"]').val();
			        var pricelist_id = $('input[name="pricelist"]').val();

			        const display_price = await ajax.rpc('/getDisplayPrice',{
			        		'add_qty': qty,
			        		'product_id': product_id,
			        		'product_template_id': product_template_id,
			        		'pricelist_id': pricelist_id,
			            }
                    )
                
			        var newhtml = `<i class="fa fa-shopping-cart"></i> Agregar $${display_price.toFixed(2)}`
                
			        add_button.html(newhtml)
                });
                // Change UOM
                $("select[name='uom_id']").on("change", async function(event) {
                    changeAmount();
                });
                // Close Quick View
                $(".qv_close").click(function() {
                    $(".quick_cover").empty(data);
                    $(".zoomContainer").remove();
                });
            });
        }

    })

    function changeAmount() {
        setTimeout(async function() {
            var uom = $('#uom_id').find("option:selected").data("uom_id");
            if (!uom) return
            const factor = await ajax.rpc('/getUomFactor', { 'uom_id': uom, })
            $('input[name="add_qty"]').val((1/factor).toFixed(2)).trigger('change');
        }, 300);
    }
    
    core.action_registry.add('pleni_shop.custom_quickView', publicWidget);

    return publicWidget;

});