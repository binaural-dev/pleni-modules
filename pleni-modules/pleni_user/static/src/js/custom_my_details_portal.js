odoo.define('pleni_user.custom_my_details_portal', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    const core = require('web.core');
    var _t = core._t;


    publicWidget.registry.portalDetails = publicWidget.Widget.extend({
        selector: '.o_portal_details',
        events: {
            'change select[name="company_type"]': '_onChangeCompanyType',
            'change .document_type': '_onChangeDocumentType',
            'change .identification_document': '_onChangeDocumentId',
            'change select[name="country_id"]': '_onCountryChange',
            'change select[name="state_id"]': '_onChangeState',
            'change select[name="municipality_id"]': '_onChangeMunicipality',
        },
        /**
         * @override
         */
        start: function () {
            this._onChangeCompanyType();
            this._onCountryChange();
            var def = this._super.apply(this, arguments);
            return def;
        },
        _onChangeCompanyType:  function () {
            const inputCompanyTypeSelector = $("select[name='company_type']");
            const documentType = $(".document_type");
            const documentId = $(".identification_document");
            const nationalityId = document.getElementById('nationality');
            const divContainerNationalityField = document.getElementById('nationality_id');
            const identificationId = document.getElementById('identification_id');
            const divContainerIdentificationIdField = document.getElementById('identification_id_id');
            const labelCompany = document.getElementById('label_company');
            const labelPerson = document.getElementById('label_person');
            const divContainerCommercialNameField = document.getElementById('field_commercial_name');

            const rifId = document.getElementById('rif');
            const divContainerRifId = document.getElementById('rif_id');

            console.log('#=============== ByName ===============#');
            console.log(documentType[0].value);
            console.log(documentId[0].value);
            let rif = rifId.value.split("-");

            if(inputCompanyTypeSelector[0].value === 'company'){
                if(rifId.value){
                    let rif_type = rif[0];
                    let rif_document = rif[1]
                    documentType[0].value = rif_type;
                    documentId[0].value = rif_document;
                }
                labelCompany.removeAttribute('style');
                labelPerson.setAttribute('style', 'display: none;');
                divContainerCommercialNameField.removeAttribute('style');
                documentType.attr('name', 'rif_type');
                documentId.attr('name', 'identification_rif');
            }

            if(inputCompanyTypeSelector[0].value === 'person'){
                if(nationalityId.value && identificationId.value){
                    documentType[0].value = nationalityId.value;
                    documentId[0].value = identificationId.value;
                }
                labelCompany.setAttribute('style', 'display: none;');
                labelPerson.removeAttribute('style');
                divContainerCommercialNameField.setAttribute('style', 'display: none;');
                documentType.attr('name', 'document_type');
                documentId.attr('name', 'identification_document');
            }

            /*if (inputCompanyTypeSelector === 'company') {
                divContainerRifId.setAttribute('style', 'display: block;');
                rifId.setAttribute('style', 'display: block;');
                rifId.setAttribute('required', '');

                divContainerNationalityField.setAttribute('style', 'display: none;');
                nationalityId.removeAttribute('required');

                divContainerIdentificationIdField.setAttribute('style', 'display: none;');
                identificationId.removeAttribute('required');


            } else if (inputCompanyTypeSelector === 'person') {
                divContainerNationalityField.setAttribute('style', 'display: block;');
                nationalityId.setAttribute('style', 'display: block;');
                nationalityId.setAttribute('required', '');

                divContainerIdentificationIdField.setAttribute('style', 'display: block;');
                identificationId.setAttribute('style', 'display: block;');
                identificationId.setAttribute('required', '');

                divContainerRifId.setAttribute('style', 'display: none;');
                rifId.removeAttribute('required');

            }*/

        },
        _onChangeDocumentType: function () {
            const inputCompanyTypeSelector = $("select[name='company_type']");
            const documentType = $(".document_type");
            const documentId = $(".identification_document");
            const nationalityId = document.getElementById('nationality');
            const divContainerNationalityField = document.getElementById('nationality_id');
            const identificationId = document.getElementById('identification_id');
            const divContainerIdentificationIdField = document.getElementById('identification_id_id');
            const labelCompany = document.getElementById('label_company');
            const labelPerson = document.getElementById('label_person');
            const divContainerCommercialNameField = document.getElementById('field_commercial_name');

            const rifId = document.getElementById('rif');
            const divContainerRifId = document.getElementById('rif_id');

            let rif = rifId.value.split('-');

            if(documentType[0].value === 'V' || documentType[0].value === 'E' || documentType[0].value === 'P'){

                inputCompanyTypeSelector[0].value = 'person';
                documentType.attr('name', 'document_type');
                documentId.attr('name', 'identification_document');
                nationalityId.value = documentType[0].value;
                documentId[0].value = identificationId.value;
                labelCompany.setAttribute('style', 'display: none;');
                labelPerson.removeAttribute('style');
                divContainerCommercialNameField.setAttribute('style', 'display: none;');

            }else{

                inputCompanyTypeSelector[0].value = 'company';
                documentType.attr('name', 'rif_type');
                documentId.attr('name', 'identification_rif');
                rif[0] = documentType[0].value;
                documentId[0].value = rif[1];
                rifId.value = `${documentType[0].value}-${documentId[0].value}`;
                labelCompany.removeAttribute('style');
                labelPerson.setAttribute('style', 'display: none;');
                divContainerCommercialNameField.removeAttribute('style');

            }

        },
        _onChangeDocumentId: function () {
            const inputCompanyTypeSelector = $("select[name='company_type']");
            const documentType = $(".document_type");
            const documentId = $(".identification_document");
            const nationalityId = document.getElementById('nationality');
            const divContainerNationalityField = document.getElementById('nationality_id');
            const identificationId = document.getElementById('identification_id');
            const divContainerIdentificationIdField = document.getElementById('identification_id_id');
            const labelCompany = document.getElementById('label_company');
            const labelPerson = document.getElementById('label_person');
            const divContainerCommercialNameField = document.getElementById('field_commercial_name');

            const rifId = document.getElementById('rif');
            const divContainerRifId = document.getElementById('rif_id');

            let rif = rifId.value.split('-');

            if(documentType[0].value === 'V' || documentType[0].value === 'E' || documentType[0].value === 'P'){

                documentType[0].value = nationalityId.value;
                identificationId.value = documentId[0].value;
                console.log(`${documentType[0].value}-${documentId[0].value}`);
                console.log(`${nationalityId.value}-${identificationId.value}`);

            }else{

                documentType[0].value = rif[0];
                rif[1] = documentId[0].value;
                rifId.value = `${documentType[0].value}-${documentId[0].value}`;

            }
        },
        _onCountryChange: async function () {
            const inputCountryId = $("select[name='country_id']").val();
            const inputStateId = $("select[name='state_id']").val();
            const allCountries = await ajax.rpc('/getStatesById', {'input_country_id': 238});
            const stateId = document.getElementById('state_select');
            $('#state_select').empty()
            allCountries.forEach(e => {
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
            const inputStateId = $("select[name='state_id']").val();
            const inputMunicipalityId = $("select[name='municipality_id']").val();
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
            this._onChangeMunicipality()
        },
        _onChangeMunicipality: async function() {
            const inputMunicipalityId = $("select[name='municipality_id']").val();
            const inputParishId = $("select[id='parish_select']").val();
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
    });

    publicWidget.registry.websiteSaleValidate = publicWidget.Widget.extend({
        selector: 'div.oe_website_sale_tx_status[data-order-id]',
    
        /**
         * @override
         */
        start: function () {
            var def = this._super.apply(this, arguments);
            this._poll_nbr = 0;
            this._paymentTransationPollStatus();
            return def;
        },
    
        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _paymentTransationPollStatus: function () {
            var self = this;
            this._rpc({
                route: '/shop/payment/get_status/' + parseInt(this.$el.data('order-id')),
            }).then(function (result) {
                self._poll_nbr += 1;
                if (result.recall) {
                    var $message = $(result.message);
                    var $warning =  $("<i class='fa fa-warning' style='margin-right:10px;'>");
                    $warning.attr("title", _t("We are waiting for confirmation from the bank or the payment provider"));
                    $message.find('span:first').prepend($warning);
                    result.message = $message.html();
                }
                self.$el.html(result.message);
            });
        },
    });

    core.action_registry.add('pleni_user.custom_my_details_portal', publicWidget);

    function session_expired(cm) {
        return {
            display: function () {
                const notif = {
                    type: _t("Debes iniciar sesión"),
                    message: "Para continuar con la experiencia de comprar en Pleni, te redireccionaremos a la vista de iniciar sesión",
                };
                const options = {
                    buttons: [{
                        text: _t("Ok"),
                        click: () => window.location = "/web/login",
                        close: true
                    }],
                };
                cm.show_warning(notif, options);
            }
        };
    }

    core.crash_registry.add('odoo.http.SessionExpiredException', session_expired);
    core.crash_registry.add('werkzeug.exceptions.Forbidden', session_expired);

    return publicWidget;

});