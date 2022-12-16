odoo.define('3mit_hide_po_ecommerce.hide_po', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');

    publicWidget.registry.PortalHomeCounters.include({
        /**
         * @override
         */
        start: async function () {
            let def = this._super.apply(this, arguments);
            this._updateCounters();
            let poElement = document.querySelector('[title="Ordenes de Compra"]');

            if (poElement != null) {
                await poElement.setAttribute('style', 'display: none !important;');
            }
            return def;
        },

    });

});
