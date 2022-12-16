odoo.define('pleni_shop.custom_handleAdd', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    'website_uom_select_suggetion_spt.MultiUomWebsiteSale'
    const core = require('web.core');
    require('website_sale.website_sale');

    publicWidget.registry.WebsiteSale.include({
        /**
        * @override
        */
        _handleAdd: async function ($form) {
           var self = this;
           this.$form = $form;
           var productSelector = [
               'input[type="hidden"][name="product_id"]',
               'input[type="radio"][name="product_id"]:checked'
           ];
           var productReady = this.selectOrCreateProduct(
               $form,
               parseInt($form.find(productSelector.join(', ')).first().val(), 10),
               $form.find('.product_template_id').val(),
               false
           );
           var uom = $('#uom_id').find("option:selected").data("uom_id");
           const factor = await this._rpc({
               route: '/getUomFactor',
               params: {
                   'uom_id': uom,
               },
           })
           
           return productReady.then(function (productId) {
               $form.find(productSelector.join(', ')).val(productId);
               self.rootProduct = {
                   product_id: productId,
                   quantity: (parseFloat($form.find('input[name="add_qty"]').val())*factor).toFixed(0) || 1,
                   uom_id: parseInt($form.find('#uom_id').find(':selected').data('uom_id')),
                   product_custom_attribute_values: self.getCustomVariantValues($form.find('.js_product')),
                   variant_values: self.getSelectedVariantValues($form.find('.js_product')),
                   no_variant_attribute_values: self.getNoVariantAttributeValues($form.find('.js_product'))
               };
               return self._onProductReady();
           });
        },
    })    

    core.action_registry.add('pleni_shop.custom_handleAdd', publicWidget);

    return publicWidget;

});