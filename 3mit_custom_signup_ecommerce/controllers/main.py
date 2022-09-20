# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import _, tools
from odoo.addons.web.controllers.main import Home
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo import http, api, SUPERUSER_ID
from odoo.http import request, route
import json


class AuthSignupHome(Home):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'company_type', 'people_type_company',
                                                     'people_type_individual', 'country_id', 'nationality', 'identification_id',
                                                     'rif', 'mobile', 'state_id', 'municipality_id', 'parish_id', 'street',
                                                     'street2', 'city', 'zip', 'ref_point', 'dispatcher_instructions', 'commercial_name')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def get_auth_signup_qcontext(self):
        """ Shared helper returning the rendering context for signup and reset password """
        NEW_SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                                      'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                                      'password', 'confirm_password', 'city', 'country_id', 'lang',
                                      'login', 'name', 'password', 'company_type', 'people_type_company',
                                      'people_type_individual', 'country_id', 'nationality', 'identification_id',
                                      'rif', 'mobile', 'state_id', 'municipality_id', 'parish_id', 'street',
                                      'street2', 'city', 'zip', 'ref_point', 'dispatcher_instructions',
                                      'commercial_name'}

        qcontext = {k: v for (k, v) in request.params.items() if k in NEW_SIGN_UP_REQUEST_PARAMS}
        qcontext.update(self.get_auth_signup_config())
        if not qcontext.get('token') and request.session.get('auth_signup_token'):
            qcontext['token'] = request.session.get('auth_signup_token')
        if qcontext.get('token'):
            try:
                # retrieve the user info (name, login or email) corresponding to a signup token
                token_infos = request.env['res.partner'].sudo().signup_retrieve_info(qcontext.get('token'))
                for k, v in token_infos.items():
                    qcontext.setdefault(k, v)
            except:
                qcontext['error'] = _("Invalid signup token")
                qcontext['invalid_token'] = True
        return qcontext


class GetStatedById(http.Controller):
    @http.route('/getStatesById', auth='none', type='json', cors='*')
    def get_states_by_id(self):
        request_pos = json.loads(request.httprequest.data)
        env = api.Environment(http.request.cr, SUPERUSER_ID, {})
        all_states = []
        if request_pos.get('params'):
            if 'input_country_id' in request_pos.get('params'):
                country_id = request_pos.get('params').get('input_country_id')
                if country_id is not None:
                    state_ids = env['res.country.state'].sudo().search([('country_id', '=', int(country_id))])
                    if state_ids:
                        all_states = [{'id': state.id, 'name': state.name} for state in state_ids]
        return all_states


class GetMunicipalitiesById(http.Controller):
    @http.route('/getMunicipalitiesById', auth='none', type='json', cors='*')
    def get_municipalities_by_id(self):
        request_pos = json.loads(request.httprequest.data)
        env = api.Environment(http.request.cr, SUPERUSER_ID, {})
        all_municipalities = []
        if request_pos.get('params'):
            if 'input_state_id' in request_pos.get('params'):
                state_id = request_pos.get('params').get('input_state_id')
                if state_id is not None:
                    municipality_ids = env['res.country.state.municipality'].sudo().search([('state_id', '=', int(state_id))])
                    if municipality_ids:
                        all_municipalities = [{'id': municipality.id, 'name': municipality.name} for municipality in municipality_ids]
        return all_municipalities


# class GetDefaultCountry(http.Controller):
#     @http.route('/getDefaultCountry', auth='none', type='json', cors='*')
#     def get_municipalities_by_id(self):
#         env = api.Environment(http.request.cr, SUPERUSER_ID, {})
#         country_default = env['res.country'].sudo().search(['|', '|', ('id', '=', 238), ('name', '=ilike', 'Venezuela'), ('code', '=', 'VE')])
#         return {'id': country_default.id, 'name': country_default.name, 'code': country_default.code}


class GetParishesById(http.Controller):
    @http.route('/getParishesById', auth='none', type='json', cors='*')
    def get_parishes_by_id(self):
        request_pos = json.loads(request.httprequest.data)
        env = api.Environment(http.request.cr, SUPERUSER_ID, {})
        all_parishes = []
        if request_pos.get('params'):
            if 'input_municipality_id' in request_pos.get('params'):
                municipality_id = request_pos.get('params').get('input_municipality_id')
                if municipality_id is not None:
                    parish_ids = env['res.country.state.municipality.parish'].sudo().search([('municipality_id', '=', int(municipality_id))])
                    if parish_ids:
                        all_parishes = [{'id': parish.id, 'name': parish.name} for parish in parish_ids]
        return all_parishes


class CustomerPortal(CustomerPortal):

    MANDATORY_BILLING_FIELDS = ['name', 'mobile', 'email', 'street', 'city', 'country_id', 'municipality_id', 'parish_id', 'street2', 'street' ]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", 'company_type', 'rif', 'nationality', 'identification_id', 'commercial_name', 'rif_type', 'identification_rif', 'document_type', 'identification_document']

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        municipalities = request.env['res.country.state.municipality'].sudo().search([])
        parishes = request.env['res.country.state.municipality.parish'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'municipalities': municipalities,
            'parishes': parishes,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error para rif e identificacion
        if data.get('company_type') == 'company' and not data.get("rif"):
            error["rif"] = 'error'
            error_message.append(_('Las compañias deben registrar su rif.'))

        if data.get('company_type') == 'person' and not data.get('identification_id'):
            error["identification_id"] = 'error'
            error_message.append(_('Debe ingresar su documento.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message
