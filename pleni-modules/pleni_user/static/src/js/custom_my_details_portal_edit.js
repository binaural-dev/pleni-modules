odoo.define('pleni_user.custom_my_details_portal_edit', function (require) {
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

    publicWidget.registry.portalDetailsEdit = publicWidget.Widget.extend({
        selector: '.o_portal_details_address',
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
            const inputStateId = $("input[name='state_id_input']").val();
            const allCountries = await ajax.rpc('/getStatesById', {'input_country_id': 238});
            const allCountriesFiltered = allCountries.filter(item => allowedStates.includes(item.name));
            const stateId = document.getElementById('state_select');
            $('#state_select').empty()
            allCountriesFiltered.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                if (String(inputStateId) === String(e.id)) {
                    opt.setAttribute('selected', true)
                }
                stateId.appendChild(opt);
            });
            this._onChangeState()
        },
        _onChangeState: async function () {
            const inputStateIdInput = $("input[name='state_id_input']").val();
            const inputStateIdSelect = $("select[name='state_id']").val();
            const inputStateId = (inputStateIdInput == inputStateIdSelect)? inputStateIdInput:inputStateIdSelect
            const inputMunicipalityId = $("input[name='municipality_id_input']").val();
            const allMunicipalities = await ajax.rpc('/getMunicipalitiesById', {'input_state_id': inputStateId});
            const municipalityId = document.getElementById('municipality_select');
            $('#municipality_select').empty()
            allMunicipalities.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                if (String(inputMunicipalityId) === String(e.id)) {
                    opt.setAttribute('selected', true)
                }
                municipalityId.appendChild(opt);
            });
            this._onChangeCity();
            this._onChangeMunicipality();
        },

        _onChangeMunicipality: async function() {
            const inputMunicipalityIdInput = $("input[name='municipality_id_input']").val();
            const inputMunicipalityIdSelect = $("select[name='municipality_id']").val();
            const inputMunicipalityId = (inputMunicipalityIdInput == inputMunicipalityIdSelect)? inputMunicipalityIdInput:inputMunicipalityIdSelect
            const inputParishId = $("input[name='parish_id_input']").val();
            const allParishes = await ajax.rpc('/getParishesById', {'input_municipality_id': inputMunicipalityId});
            const parishId = document.getElementById('parish_select');
            $('#parish_select').empty()
            allParishes.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
                opt.innerHTML = e.name;
                if (String(inputParishId) === String(e.id)) {
                    opt.setAttribute('selected', true)
                }
                parishId.appendChild(opt);
            });
        },

        _onChangeCity: async function () {
            const inputStateIdInput = $("input[name='state_id_input']").val();
            const inputStateIdSelect = $("select[name='state_id']").val();
            const inputStateId = (inputStateIdInput == inputStateIdSelect)? inputStateIdInput:inputStateIdSelect
            const allCities = await ajax.rpc('/getCitiesById', {'input_state_id': inputStateId});
            const inputCityId = $("input[name='city_id_input']").val();
            const cityId = document.getElementById('city_select');
            $('#city_select').empty()
            allCities.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.name;
                opt.innerHTML = e.name;
                if (String(inputCityId) === String(e.name)) {
                    opt.setAttribute('selected', true)
                }
                cityId.appendChild(opt);
            });
        },
    });


    core.action_registry.add('pleni_user.custom_my_details_portal_edit', publicWidget);

    return publicWidget;

});