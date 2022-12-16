odoo.define('3mit_uom_fixing_ecommerce.custom_onClickAddCartJson', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    const core = require('web.core');

    publicWidget.registry.WebsiteSale.include({
        /**
        * @override
        */
        _onClickAddCartJSON: async function (ev){
            if (window?.location?.href.includes('cart')) {
                this.onClickAddCartJSON(ev);
                return false
            }
            var qty = parseFloat($('input[name="add_qty"]').val());
            var uom = $('#uom_id').find("option:selected").data("uom_id");
            if (!uom) return
            const factor = await this._rpc({
                route: '/getUomFactor',
                params: {
                    'uom_id': uom,
                },
            })
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var newQuantity = ($link.has(".fa-minus").length ? -1/factor : 1/factor) + qty;
            var newQty = newQuantity > min ? (newQuantity < max ? newQuantity : max) : min;
            if (newQty !== qty) {
                $('input[name="add_qty"]').val(newQty.toFixed(2)).trigger('change');
            }
            return false
        },
    });

    core.action_registry.add('3mit_uom_fixing_ecommerce.custom_onClickAddCartJson', publicWidget);

    return publicWidget;

});
