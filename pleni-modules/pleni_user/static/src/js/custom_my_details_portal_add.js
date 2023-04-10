odoo.define('pleni_user.custom_my_details_portal_add', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    const core = require('web.core');
    var _t = core._t;

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

    publicWidget.registry.portalDetailsAdd = publicWidget.Widget.extend({
        selector: '.o_portal_details_address_add',
        events: {
            'change select[name="country_id"]': '_onCountryChange',
            'change select[name="state_id"]': '_onChangeState',
            'change select[name="municipality_id"]': '_onChangeMunicipality',
        },

        /**
         * @override
         */
        start: function () {
            // this._onChangeCompanyType();
            this._onCountryChange();
            var def = this._super.apply(this, arguments);
            return def;
        },

        _onCountryChange: async function () {
            const allCountries = await ajax.rpc('/getStatesById', {'input_country_id': 238});
            const allCountriesFiltered = allCountries.filter(item => allowedStates.includes(item.name));
            const stateId = document.getElementById('state_select');
            $('#state_select').empty()
            allCountriesFiltered.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                stateId.appendChild(opt);
            });
            this._onChangeState()
        },
        _onChangeState: async function () {
            const inputStateId = $("select[name='state_id']").val();
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

        _onChangeCity: async function () {
            const inputStateId = $("select[name='state_id']").val();
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
    });


    core.action_registry.add('pleni_user.custom_my_details_portal_add', publicWidget);

    return publicWidget;

});