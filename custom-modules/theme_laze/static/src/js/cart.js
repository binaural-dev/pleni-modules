odoo.define('theme_laze.cart', function (require) {
"use strict";

var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
var rpc = require('web.rpc')

// Cart Popover
publicWidget.registry.AtharvaCart = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    events: {
        'click .js_delete_product' : '_onClickDeleteProductCart',
    },
    init: function () {
        this._super.apply(this, arguments);
    },
    _onClickRemoveProduct: function (ev) {
        ev.preventDefault();
        $(ev.currentTarget).siblings().find('.js_quantity').val(0).trigger('change');
    },
    _onUpdateQty: function(ev){
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find("input");
        var min = parseFloat($input.data("min") || 0);
        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
        var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
            let quantity =  $(ev.target).closest('.css_quantity').find('input')
            ev.currentTarget = $(quantity);
            var cartUpdate = new publicWidget.registry.AtharvaCart();
            cartUpdate._onChangeQty(ev);
        }
        return false;
    },
    _onChangeQty: function (ev){
        var $input = $(ev.currentTarget);
        var self = this;
        $input.data('update_change', false);
        var value = parseInt($input.val() || 0, 10);
        if (isNaN(value)) {
            value = 1;
        }
        var line_id = parseInt($input.data('line-id'), 10);
        let loading = document.getElementById('loading_pleni')
        loading.classList.add('loading-pleni')
        rpc.query({
            route: "/shop/cart/update_json",
            params: {
                line_id: line_id,
                product_id: parseInt($input.data('product-id'), 10),
                set_qty: value
            },
        }).then(function (data) {
            $input.data('update_change', false);
            var check_value = parseInt($input.val() || 0, 10);
            if (isNaN(check_value)) {
                check_value = 1;
            }
            if (value !== check_value) {
                $input.trigger('change');
                return;
            }
            if (!data.cart_quantity) {
                return window.location = '/shop';
            }
            wSaleUtils.updateCartNavBar(data);
            $input.val(data.quantity);
            $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
            $.get("/shop/cart", {
                type: 'cart_lines_popup',
            }).then(function(data) {
                $(".cart_lines_popup").empty().html(data);
                $("a.js_add_cart_json").on('click', function(ev) {
                    ev.preventDefault();
                    //self._onUpdateQty(ev)
                });
                $(".js_quantity[data-product-id]").off('change').on('change',function(ev) {
                    ev.preventDefault();
                    self._onChangeQty(ev)
                });
                $("a.js_delete_product").off('click').on('click', function(ev) {
                    ev.preventDefault();
                    self._onClickRemoveProduct(ev)
                });

                $("select[class='cart_type_select']").off('change').on("change", async function(event) {
                    var cartUpdate = new publicWidget.registry.WebsiteSale();
                    cartUpdate._onChangeUomSelection(event);
                });
            });
            loading.classList.remove('loading-pleni')
        });
    },
    _onClickDeleteProductCart: function(ev) {
        ev.preventDefault();
        let quantity =  $(ev.target).closest('tr').find('input')
        ev.currentTarget = $(quantity);

        var $input = $(quantity);
        var value = parseInt($input.val());

        if (!isNaN(value) && value >=0) {
            var cartUpdate = new publicWidget.registry.AtharvaCart();
            cartUpdate._onChangeQty(ev);
        }
    },
});

publicWidget.registry.atharvaCartLink = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    events: {
        'click header #my_cart .my_cart_btn': '_onCartClick',
        'click .cart_lines_popup .m_c_close': '_onCloseClick',
        'input .js_quantity.form-control.quantity': '_onChangeQty',
        'click a.js_delete_product': '_onRemoveCartItemList',
        'click a.js_add_cart_json': '_clickChangeQuantity'
    },
    _onCartClick: function (ev) {
        var $target = $(ev.currentTarget);
        $.get("/shop/cart", {type: 'cart_lines_popup'}).then(function(data){
            var cartUpdate = new publicWidget.registry.AtharvaCart();
            if(data.trim()){
                /*var $mini_cart_popup = $target.parents("header").find(".cart_lines_popup");
                $mini_cart_popup.empty().append(data.trim()).addClass("show_mini_cart");
                $("body").addClass("cart-open-on-body");*/

                window.location.href='/shop/cart?';

                $("a.js_add_cart_json").off('click').on('click', function(ev) {
                    ev.preventDefault();
                    //cartUpdate._onUpdateQty(ev)
                });

                $(".js_quantity[data-product-id]").off('change').on('change',function(ev) {
                    ev.preventDefault();
                    cartUpdate._onChangeQty(ev)
                });
            }
        });
        ev.stopPropagation();
    },
    _onCloseClick: function (ev) {
        $(ev.currentTarget).parents(".cart_lines_popup").removeClass("show_mini_cart");
        $("body").removeClass("cart-open-on-body");
    },

    _onChangeQty: function (ev) {
        var $input = $(ev.currentTarget);
        var value = parseInt($input.val());

        if (!isNaN(value) && value >=0) {
            var cartUpdate = new publicWidget.registry.AtharvaCart();
            cartUpdate._onChangeQty(ev);
        }
    },

    _onRemoveCartItemList: function (ev) {
        var cartUpdate = new publicWidget.registry.AtharvaCart();
        ev.preventDefault();
        cartUpdate._onClickRemoveProduct(ev);
    },

    _clickChangeQuantity: function(event) {
        //event.preventDefault();
        console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        var cartUpdate = new publicWidget.registry.AtharvaCart();
        cartUpdate._onUpdateQty(event);
    }
});
});
