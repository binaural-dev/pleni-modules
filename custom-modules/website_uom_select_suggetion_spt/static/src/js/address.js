odoo.define('pleni.website_sale_bin', function (require) {
    'use strict';

    var core = require('web.core');
    const ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    const VariantMixin = require('sale.VariantMixin');

    const allowedStates = [
        'Distrito Capital',
        'Miranda',
        'Aragua',
        'Carabobo',
        'Vargas',
        'Lara',
        'Yaracuy',
        'Portuguesa'
    ]


    publicWidget.registry.AtharvaCart.include({
        selector: '#form1',
        events: {
            'change #country_select': '_onChangeCountry',
            'change select[id="state_select"]': '_onChangeState',
            'change #municipality_select': '_onChangeMunicipality',
        },
        /**
         * @constructor
         */
        init: function () {
            const countryId = document.querySelector('#country_select option[value="238"]');
            if (countryId != null) {
                countryId.setAttribute("selected", "selected");
                this._onChangeCountry();
            }
        },
       
        /**
     * @private
     */
        _onChangeCountry: async function () {
            const inputCountryId = $("select[name='country_id']").val();
            const allCountries = await ajax.rpc('/getStatesById', {'input_country_id': 238});
            const allCountriesFiltered = allCountries.filter(item => allowedStates.includes(item.name));
            const stateId = document.getElementById('state_select');
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const user = urlParams.get('partner_id')
            console.log(queryString);
            console.log(user);
            $('#state_select').empty()
            allCountriesFiltered.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                stateId.appendChild(opt);
            });
            this._onChangeState()
        },

        /**
         * @private
         */
        _onChangeState: async function () {
            const inputStateId = $("select[id='state_select']").val();
            const allMunicipalities = await ajax.rpc('/getMunicipalitiesById', {'input_state_id': inputStateId});
            const municipalityId = document.getElementById('municipality_select');
            $('#municipality_select').empty()
            allMunicipalities.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                municipalityId.appendChild(opt);
            });
            this._onChangeCity();
            this._onChangeMunicipality();
        },

        _onChangeCity: async function () {
            const inputStateId = $("select[id='state_select']").val();
            const allCities = await ajax.rpc('/getCitiesById', {'input_state_id': inputStateId});
            const cityId = document.getElementById('city_select');
            $('#city_select').empty()
            allCities.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.name;
                opt.innerHTML = e.name;
                cityId.appendChild(opt);
            });
        },

        /**
         * @private
         */
        _onChangeMunicipality: async function() {
            const inputMunicipalityId = $("select[name='municipality_id']").val();
            const allParishes = await ajax.rpc('/getParishesById', {'input_municipality_id': inputMunicipalityId});
            const parishId = document.getElementById('parish_select');
            $('#parish_select').empty()
            allParishes.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                parishId.appendChild(opt);
            });
        },
    
        
    });
  
});
