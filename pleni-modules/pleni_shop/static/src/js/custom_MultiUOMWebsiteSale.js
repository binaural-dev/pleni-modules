odoo.define('pleni_shop.custom_MultiUOMWebsiteSale', function (require) {
    'use strict';

    var MultiUOMWebsiteSale = require('website_uom_select_suggetion_spt.MultiUomWebsiteSale');

    const publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    const core = require('web.core');

    publicWidget.registry.MultiUOMWebsiteSale.include({
        /**
        * @override
        */
		onChangeUOM: async function(ev){
			var qty = parseFloat($('input[name="add_qty"]').val());
            this.onChangeVariant(ev);
            let zero = 0
            $('input[name="add_qty"]').val(zero.toFixed(2)).trigger('change');
        }

    })    


    core.action_registry.add('pleni_shop.custom_MultiUOMWebsiteSale', publicWidget);

    return publicWidget;

});