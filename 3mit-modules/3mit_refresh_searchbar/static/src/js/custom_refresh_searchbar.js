odoo.define('3mit_refresh_searchbar.custom_refresh_searchbar', function (require) {
'use strict';

    const publicWidget = require('web.public.widget');

    publicWidget.registry.productsSearchBar.include({
        /**
     * @private
     */
        _getInputSearch: async function () {
            return $('.search-query');
        },

        /**
         * @private
         */
        _onInput: async function () {
            const inputSearch = await this._getInputSearch()
            setTimeout(function(){
                window.location = '/shop?' + inputSearch.attr('name') + '=' + encodeURIComponent(inputSearch.val());
            }, 2500);
        },
    })

    publicWidget.registry.customWebsiteSaleCategory = publicWidget.Widget.extend({
        selector: '#o_shop_collapse_category',
        events: {
            'click .nav-item': '_onClickShopCategory',
        },
        /**
         * @private
         */
        _onClickShopCategory: function () {
            // ! Este codigo esta obsoleto. Se debe reestructurar para volver a obtener su funcionalidad
            let activeElement = document.activeElement
            console.log(activeElement)

            const searchInclude = activeElement.href?.includes('?')
            console.log(searchInclude)
            if (searchInclude) {
                let newHref = activeElement.href.split('?')
                activeElement.href = newHref[0]
            }

        },

});

});
