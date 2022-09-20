"use strict";

odoo.define("website_uom_select_suggetion_spt.MultiUOMOptionalProductsModal", function (require) {
  "use strict";

  var ajax = require('web.ajax');

  var OptionalProductsModal = require('sale_product_configurator.OptionalProductsModal');

  OptionalProductsModal.extend({
    /**
     * @override
     */
    willStart: function willStart() {
      debugger;

      var res = this._super.apply(this, arguments);

      var self = this;
      debugger;

      var uri = this._getUri("/sale_product_configurator/show_optional_products");

      var getModalContent = ajax.jsonRpc(uri, 'call', {
        product_id: self.rootProduct.product_id,
        variant_values: self.rootProduct.variant_values,
        pricelist_id: self.pricelistId || false,
        add_qty: self.rootProduct.quantity,
        kwargs: {
          context: _.extend({
            'quantity': self.rootProduct.quantity
          }, this.context)
        }
      }).then(function (modalContent) {
        if (modalContent) {
          var $modalContent = $(modalContent);
          $modalContent = self._postProcessContent($modalContent);
          self.$content = $modalContent;
        } else {
          self.trigger('options_empty');
          self.preventOpening = true;
        }
      });

      var parentInit = self._super.apply(self, arguments);

      return Promise.all([getModalContent, parentInit]);
    }
  });
});