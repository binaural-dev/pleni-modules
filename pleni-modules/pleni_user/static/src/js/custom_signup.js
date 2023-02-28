odoo.define('pleni_user.custom_signup', function (require) {
    'use strict';

    const authSignup = require('web.public.widget');
    const ajax = require('web.ajax');
    const core = require('web.core');

    const patternVE = new RegExp("^[0-9]{6,8}$");
    const patternJG = new RegExp("^[0-9]{5,9}$");
    const patternP = new RegExp("^(?!^0+\$)[a-zA-Z0-9]{6,9}");
    const patternName = /^[a-zA-Z\s\.]+$/
    const patternBusinessName = new RegExp("^[ÁÀÂÄÇÉÈÊËÍÌÎÏÓÒÔÖÙÛÜÚÑßĄA-Z'|a-záàâäçéèêëíìîïóòôöùûüúñ'\\-][ÁÀÂÄÇÉÈÊËÍÌÎÏÓÒÔÖÙÛÜÚÑßĄA-Z'\\-a-záàâäçéèêëíìîïóòôöùûüúñ0-9, ]+((\\.|\\s)+[ÁÀÂÄÇÉÈÊËÍÌÎÏÓÒÔÖÙÛÜÚÑßĄA-Z'\\-|a-záàâäçéèêëíìîïóòôöùûüúñ|0-9|\\., ]+)*\$")
    const patternEmail = /^[a-zA-Z0-9]+(?:[_.-][a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:[_.-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,3}$/;
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

    authSignup.registry.SignUpForm = authSignup.Widget.extend({
        selector: '.oe_website_login_container',
        events: {
            'change #prefix_vat': '_onChangeNewNationality',
            'input #vat': '_onChangeNewIdentificationId',
            'change #country_select': '_onChangeCountry',
            'change #state_select': '_onChangeState',
            'change #municipality_select': '_onChangeMunicipality',
            'click .toggle-password': '_showEyesPassword',
            'click .toggle-confirm-password': '_showEyesConfirmPassword',
            'input #name' : '_onChangeName',
            'input #commercial_name' : '_onChangeCommercialName',
            'input #login' : '_onChangeEmail',
            'focusout #telephone': '_onChangeTelephone',
            'input #confirm_password' : '_onChangeConfirmPassword',
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
            checkForm();
        },

        /**
         * @private
         */
        _onChangeNewNationality: function(){
            const newNationalityId = document.getElementById('prefix_vat').value;
            const inputCommercialName = document.getElementById('field_commercial_name');
            const commercialName = document.getElementById('commercial_name');
            const labelPerson = document.getElementById('label_person');
            const labelCompany = document.getElementById('label_company');
            let nationalityId = document.getElementById('nationality');

            //let inputCompanyTypeSelector = document.getElementById('company_type');
            const textValidation = document.getElementById('validationIdentification');

            if (newNationalityId === 'V' || newNationalityId === 'E' || newNationalityId === 'P') {
                //inputCompanyTypeSelector.value = 'person';
                nationalityId.value = newNationalityId;
                inputCommercialName.setAttribute('style', 'display: none;');
                labelCompany.setAttribute('style', 'display: none;');
                labelPerson.removeAttribute('style');
                commercialName.removeAttribute('required');

                if (newNationalityId === 'V' || newNationalityId === 'E') {
                    matchRegrex(
                        'Debe contener solo entre 6 y 8 dígitos numéricos', 
                        patternVE, 
                        textValidation, 
                        document.getElementById('vat')
                    )
                } else {
                    matchRegrex(
                        'Debe contener entre 6 y 9 caracteres y números', 
                        patternP, 
                        textValidation, 
                        document.getElementById('vat')
                    )
                }



            } else if (newNationalityId === 'J' || newNationalityId === 'G') {
                //inputCompanyTypeSelector.value = 'company';
                inputCommercialName.setAttribute('style', 'display: block;');
                labelPerson.setAttribute('style', 'display: none;');
                labelCompany.removeAttribute('style');
                commercialName.setAttribute('required', '');


                matchRegrex(
                    'Debe contener solo entre 6 y 9 dígitos numéricos', 
                    patternJG, 
                    textValidation, 
                    document.getElementById('vat')
                )
            }

        },

        /**
         * @private
         */
        _onChangeNewIdentificationId: function(){
            const newNationalityId = document.getElementById('prefix_vat').value;
            const newIdentificationId = document.getElementById('vat').value;
            const inputCommercialName = document.getElementById('field_commercial_name');
            const textValidation = document.getElementById('validationIdentification');
            const commercialName = document.getElementById('commercial_name');
            const labelPerson = document.getElementById('label_person');
            const labelCompany = document.getElementById('label_company');
            let nationalityId = document.getElementById('nationality');
            let identificationId = document.getElementById('identification_id');
            // let rifId = document.getElementById('rif');
            //let inputCompanyTypeSelector = document.getElementById('company_type');


            if (newNationalityId === 'V' || newNationalityId === 'E' || newNationalityId === 'P') {
                //inputCompanyTypeSelector.value = 'person';
                nationalityId.value = newNationalityId;
                identificationId.value = newIdentificationId;
                inputCommercialName.setAttribute('style', 'display: none;');
                labelCompany.setAttribute('style', 'display: none;');
                labelPerson.removeAttribute('style');
                commercialName.removeAttribute('required');

                if (newNationalityId === 'V' || newNationalityId === 'E') {
                    matchRegrex(
                        'Debe contener solo entre 6 y 8 dígitos numéricos', 
                        patternVE, 
                        textValidation, 
                        document.getElementById('vat')
                    )
                } else {
                    matchRegrex(
                        'Debe contener entre 6 y 9 caracteres y números', 
                        patternP, 
                        textValidation, 
                        document.getElementById('vat')
                    )
                }


            } else if (newNationalityId === 'J' || newNationalityId === 'G') {
                //inputCompanyTypeSelector.value = 'company';
                // rifId.value = `${newNationalityId}-${newIdentificationId}`;
                inputCommercialName.setAttribute('style', 'display: block;');
                labelPerson.setAttribute('style', 'display: none;');
                labelCompany.removeAttribute('style');
                commercialName.setAttribute('required', '');

                matchRegrex(
                    'Debe contener solo entre 6 y 9 dígitos numéricos', 
                    patternJG, 
                    textValidation, 
                    document.getElementById('vat')
                )
            }

        },

        _onChangeName: function() {
            const name = document.getElementById('name');
            const textValidation = document.getElementById('validationName');
            matchRegrex(
                'Debe contener solo caracteres', 
                patternName, 
                textValidation, 
                name
            )
        },


        _onChangeCommercialName: function() {
            const name = document.getElementById('commercial_name');
            const textValidation = document.getElementById('validationCommercialName');
            matchRegrex(
                'Debe contener solo caracteres', 
                patternBusinessName, 
                textValidation, 
                name
            )
        },

        _onChangeEmail: async function() {
            const email = document.getElementById('login');
            document.getElementById('login').value = email.value.toLowerCase();
            const textValidation = document.getElementById('validationEmail');
            if (textValidation) {
                if (email.value.toLowerCase().match(patternEmail)) {
                    email.classList.remove("is-invalid")
                    email.classList.add("is-valid")
                    let emailSaved = await ajax.rpc('/getEmailSaved', {'email': email.value.toLowerCase()});
                    if (emailSaved) {
                        email.classList.remove("is-valid")
                        email.classList.add("is-invalid")
                        textValidation.innerText = `El correo ${email.value} se encuentra registrado`;
                    } else {
                        email.classList.remove("is-invalid")
                        email.classList.add("is-valid")
                    }
                }
                else {
                    email.classList.remove("is-valid")
                    email.classList.add("is-invalid")
                    textValidation.innerText = 'No es un email válido'
                }
            }
        },

        _onChangeTelephone: function() {
            const telephone = document.getElementById('telephone');
            const textValidation = document.getElementById('validationTelephone');
            if (!telephone.value) return;

            try {
                const parseNumber = libphonenumber.parsePhoneNumber(telephone.value)

                if (parseNumber.isValid()) {
                    telephone.classList.remove("is-invalid")
                    telephone.classList.add("is-valid")
                } else {
                    telephone.classList.remove("is-valid")
                    telephone.classList.add("is-invalid")
                    textValidation.innerText = 'No es un teléfono válido'
                }
            } catch (error) {
                console.error(error);
            }

        },

        _onChangeConfirmPassword: function() {
            const confirmPassword = document.getElementById('confirm_password');
            const password = document.getElementById('password');
            const textValidation = document.getElementById('validationConfirmPassword');

            if (textValidation) {
                if (confirmPassword.value === password.value) {
                    confirmPassword.classList.remove("is-invalid")
                    confirmPassword.classList.add("is-valid")
                } else {
                    confirmPassword.classList.remove("is-valid")
                    confirmPassword.classList.add("is-invalid")
                    textValidation.innerText = 'la Contraseña y la Confirmación de Contraseña no concuerdan';
                }
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

        _onChangeCity: async function () {
            const inputStateId = $("select[name='state_id']").val();
            const allCities = await ajax.rpc('/getCitiesById', {'input_state_id': inputStateId});
            const cityId = document.getElementById('city_select');
            $('#city_select').empty()
            allCities.forEach(e => {
                var opt = document.createElement('option');
                opt.value = e.id;
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

        _showEyesPassword: function(ev) {
            const inputPassword  = $(ev.target);
            inputPassword.toggleClass("fa-eye fa-eye-slash");

            var input = $("#password");
            if (input.attr("type") === "password") {
              input.attr("type", "text");
            } else {
              input.attr("type", "password");
            }
        },

        _showEyesConfirmPassword: function(ev) {
            const inputPassword  = $(ev.target);
            inputPassword.toggleClass("fa-eye fa-eye-slash");

            var input = $("#confirm_password");
            if (input.attr("type") === "password") {
              input.attr("type", "text");
            } else {
              input.attr("type", "password");
            }
        }
    });

    function matchRegrex(validationText = '', regrex, validationElement, inputElement) {
        if (regrex.test(inputElement.value)) {
            inputElement.classList.remove("is-invalid")
            inputElement.classList.add("is-valid")
        } else {
            inputElement.classList.remove("is-valid")
            inputElement.classList.add("is-invalid")
            validationElement.innerText = validationText
        }
    }

    function checkForm() {
        var forms = document.querySelectorAll('.needs-validation');

        // Loop over them and prevent submission
        Array.prototype.slice.call(forms).forEach(function (form) {
            
            form.addEventListener('submit', function (event) {

                Array.prototype.forEach.call(form, child => {
                    if (child.classList.contains("is-invalid")) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                });
            }, false)
        })

    }

    core.action_registry.add('pleni_user.custom_signup', authSignup);

    return authSignup;

});