// odoo.define('website_uom_select_suggetion_spt.WebsiteSaleOptions', function(require){
//     "use strict";
//     var core = require('web.core');
//     var _t = core._t;
//     var ajax = require('web.ajax');
//     var weContext = require('web_editor.context');
//     var sAnimations = require('website.content.snippets.animation');
//     var OptionalProductsModal = require('sale.OptionalProductsModal');
//     require('website_sale_options.website_sale');
//     // var ProductConfiguratorMixin = require('sale.ProductConfiguratorMixin');
//     sAnimations.registry.WebsiteSaleOptions.include({
//         /**
//          * Initializes the optional products modal
//          * and add handlers to the modal events (confirm, back, ...)
//          * @override
//          * @private
//          * @param {$.Element} $form the related webshop form
//          */
//         _handleAdd: function($form){
//             var self = this;
//             this.$form = $form;
//             this.isWebsite = true;
//             var productSelector = [
//                 'input[type="hidden"][name="product_id"]',
//                 'input[type="radio"][name="product_id"]:checked'
//             ];
//             var productReady = this.selectOrCreateProduct(
//                 $form,
//                 parseInt($form.find(productSelector.join(', ')).first().val(), 10),
//                 $form.find('.product_template_id').val(),
//                 false
//             );
//             return productReady.done(function (productId) {
//                 $form.find(productSelector.join(', ')).val(productId);
//                 self.rootProduct = {
//                     product_id: productId,
//                     quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
//                     uom_id: parseInt($form.find('#uom_id').val()),
//                     product_custom_attribute_values: self.getCustomVariantValues($form.find('.js_product')),
//                     variant_values: self.getSelectedVariantValues($form.find('.js_product')),
//                     no_variant_attribute_values: self.getNoVariantAttributeValues($form.find('.js_product'))
//                 };
//                 self.optionalProductsModal = new OptionalProductsModal($form, {
//                     rootProduct: self.rootProduct,
//                     isWebsite: true,
//                     okButtonText: _t('Proceed to Checkout'),
//                     cancelButtonText: _t('Continue Shopping'),
//                     title: _t('Add to cart')
//                 }).open();
//                 self.optionalProductsModal.on('options_empty', null, self._onModalOptionsEmpty.bind(self));
//                 self.optionalProductsModal.on('update_quantity', null, self._onOptionsUpdateQuantity.bind(self));
//                 self.optionalProductsModal.on('confirm', null, self._onModalConfirm.bind(self));
//                 self.optionalProductsModal.on('back', null, self._onModalBack.bind(self));
//                 return self.optionalProductsModal.opened();
//             });
//         },
//     });
// });
"use strict";