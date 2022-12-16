odoo.define('3mit_website_order_new_style.click_functions', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    const core = require('web.core');

    publicWidget.registry.websiteClickFunctions = publicWidget.Widget.extend({
        selector: '#js-find-father-div',
        events: {
            'click #js_button_pay_method': '_onClickButton',
            'click #js_button_after_click': '_onClickButtonAfter',
        },
        /**
         * @private
         */
         _onClickButton: function () {
            let alerta = $('.alert-dismissable');
            let boton = $('#js_button_pay_method');
            let boton_after = $('#js_button_after_click');
            for(let i=0; i<alerta.length; i++){
                alerta[i].classList.remove('d-none');
            }
            for(let i=0; i<boton.length; i++){
                boton[i].classList.add('d-none');
            }
            for(let i=0; i<boton_after.length; i++){
                boton_after[i].classList.remove('d-none');
            }
         },

         _onClickButtonAfter: function () {
            let alerta = $('.alert-dismissable');
            let boton = $('#js_button_pay_method');
            let boton_after = $('#js_button_after_click');
            for(let i=0; i<alerta.length; i++){
                alerta[i].classList.add('d-none');
            }
            for(let i=0; i<boton_after.length; i++){
                boton_after[i].classList.add('d-none');
            }
            for(let i=0; i<boton.length; i++){
                boton[i].classList.remove('d-none');
            }
         }
    }),


    core.action_registry.add('3mit_website_order_new_style.click_functions', publicWidget);

    return publicWidget;

});
