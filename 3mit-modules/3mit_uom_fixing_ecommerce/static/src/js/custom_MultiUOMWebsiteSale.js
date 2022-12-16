odoo.define('3mit_uom_fixing_ecommerce.custom_MultiUOMWebsiteSale', function (require) {
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
			// var uom = $('#uom_id').find("option:selected").data("uom_id");
            // if (!uom) return
            // const factor = await this._rpc({
            //     route: '/getUomFactor',
            //     params: {
            //         'uom_id': uom,
            //     },
            // })
			// const factorQty = parseFloat(1/factor);
			// var rest = factorQty !== 0? qty % factorQty : qty
            // var newQty = rest >= factorQty/2 ? qty + (factorQty - rest) : qty - rest;
			// if (newQty !== qty) {
            // $('input[name="add_qty"]').val(newQty.toFixed(2)).trigger('change');
            // }
        }

    })    


    core.action_registry.add('3mit_uom_fixing_ecommerce.custom_MultiUOMWebsiteSale', publicWidget);

    return publicWidget;

});
