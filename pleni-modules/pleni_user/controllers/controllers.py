# -*- coding: utf-8 -*-
from asyncio.log import logger
from odoo import _, tools, fields, http
from odoo.addons.web.controllers.main import Home
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo import http, api, SUPERUSER_ID, models
from odoo.http import request, route
import json

class AuthSignupHome(Home):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'company_type',
                                                     'country_id', 'prefix_vat', 'vat',
                                                     'mobile', 'state_id', 'municipality_id', 'street',
                                                     'street2', 'city', 'zip', 'ref_point', 'dispatcher_instructions')}
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
                                      'login', 'name', 'password', 'company_type',
                                      'country_id', 'prefix_vat', 'vat',
                                      'mobile', 'state_id', 'municipality_id', 'street',
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

    @http.route('/getEmailSaved', auth='none', type='json', cors='*')
    def get_email_saved(self):
        request_pos = json.loads(request.httprequest.data)
        emailSaved = request_pos.get('params').get('email')
        email = request.env['res.partner'].sudo().search([('email', '=', emailSaved)])
        return True if email else False


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

class GetCitiesById(http.Controller):
    @http.route('/getCitiesById', auth='none', type='json', cors='*')
    def get_cities_by_id(self):
        request_pos = json.loads(request.httprequest.data)
        env = api.Environment(http.request.cr, SUPERUSER_ID, {})
        all_cities = []
        if request_pos.get('params'):
            if 'input_state_id' in request_pos.get('params'):
                state_id = request_pos.get('params').get('input_state_id')
                if state_id is not None:
                    cities_ids = env['res.country.city'].sudo().search([('state_id', '=', int(state_id))])
                    if cities_ids:
                        all_cities = [{'id': city.id, 'name': city.name} for city in cities_ids]
        return all_cities


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
                    municipality_ids = env['res.country.municipality'].sudo().search([('state_id', '=', int(state_id))])
                    if municipality_ids:
                        all_municipalities = [{'id': municipality.id, 'name': municipality.name} for municipality in municipality_ids]
        return all_municipalities

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
                    parish_ids = env['res.country.parish'].sudo().search([('municipality_id', '=', int(municipality_id))])
                    if parish_ids:
                        all_parishes = [{'id': parish.id, 'name': parish.name} for parish in parish_ids]
        return all_parishes


class CustomerPortal(CustomerPortal):

    MANDATORY_BILLING_FIELDS = ['name', 'mobile', 'email', 'street', 'city', 'country_id', 'municipality_id', 'parish_id', 'street2', 'street' ]
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", 'company_type','commercial_name']
    FIREBASE_FIELDS = ["register_all_notification","register_specific_notification"]

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
        municipalities = request.env['res.country.municipality'].sudo().search([])
        parishes = request.env['res.country.municipality.parish'].sudo().search([])

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
        # if data.get('company_type') == 'company' and not data.get("rif"):
        #     error["rif"] = 'error'
        #     error_message.append(_('Las compañias deben registrar su rif.'))

        # if data.get('company_type') == 'person' and not data.get('identification_id'):
        #     error["identification_id"] = 'error'
        #     error_message.append(_('Debe ingresar su documento.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS + self.FIREBASE_FIELDS]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message


class WebsiteSale(http.Controller):

    @http.route(['/shop/cart/update_json'], type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            return {}

        value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty)

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template("website_sale.short_cart_summary", {
            'website_sale_order': order,
        })
        return value

class WebsiteSaleWishlist(WebsiteSale):
    def _get_pricelist_context(self):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        return pricelist_context, pricelist

    @http.route(['/shop/wishlist/add'], type='json', auth="user", website=True)
    def add_to_wishlist(self, product_id, price=False, **kw):
        if not price:
            pricelist_context, pl = self._get_pricelist_context()
            p = request.env['product.product'].with_context(pricelist_context, display_default_code=False).browse(product_id)
            price = p._get_combination_info_variant()['price']

        Wishlist = request.env['product.wishlist']
        if request.website.is_public_user():
            Wishlist = Wishlist.sudo()
            partner_id = False
        else:
            partner_id = request.env.user.partner_id.id

        wish_id = Wishlist._add_to_wishlist(
            pl.id,
            pl.currency_id.id,
            request.website.id,
            price,
            product_id,
            partner_id
        )

        if not partner_id:
            request.session['wishlist_ids'] = request.session.get('wishlist_ids', []) + [wish_id.id]

        return wish_id

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    def signup(self, values, token=None):
        """ signup a user, to either:
            - create a new user (no token), or
            - create a user for a partner (with token, but no user for partner), or
            - change the password of a user (with token, and existing user).
            :param values: a dictionary with field values that are written on user
            :param token: signup token (optional)
            :return: (dbname, login, password) for the signed up user
        """

        if token:
            # signup with a token: find the corresponding partner id
            partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
            # invalidate signup token
            partner.write({'signup_token': False, 'signup_type': False, 'signup_expiration': False})

            partner_user = partner.user_ids and partner.user_ids[0] or False

            # avoid overwriting existing (presumably correct) values with geolocation data
            if partner.country_id or partner.zip or partner.city:
                values.pop('city', None)
                values.pop('country_id', None)
            if partner.lang:
                values.pop('lang', None)

            if partner_user:
                # user exists, modify it according to values
                values.pop('login', None)
                values.pop('name', None)
                partner_user.write(values)

                if not partner_user.login_date:
                    partner_user._notify_inviter()

                return (self.env.cr.dbname, partner_user.login, values.get('password'))
            else:
                # user does not exist: sign up invited user
                values.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'email': values.get('email') or values.get('login'),
                })
                if partner.company_id:
                    values['company_id'] = partner.company_id.id
                    values['company_ids'] = [(6, 0, [partner.company_id.id])]

                    partner_user = self._signup_create_user(values)
                partner_user._notify_inviter()
        else:
            # no token, sign up an external user
            values['email'] = values.get('email') or values.get('login')

            original_values = {
                'email': values['email'],
                'name': values['name'],
                'password': values['password'],
                'lang': values['lang'],
                'login': values['email'],
                "active": True
            }

            new_user = self._signup_create_user(original_values)
            if new_user.partner_id:
                new_user.partner_id.write({
                    'company_type': values.get('company_type'),
                    'email': values.get('login'),
                    'lang': 'es_VE',
                    'country_id': 238,
                    'prefix_vat': values.get('prefix_vat'),
                    'vat': values.get('vat'),
                    'mobile': values.get('mobile'),
                    'state_id': int(values.get('state_id')),
                    'municipality_id': int(values.get('municipality_id')),
                    # 'parish_id': values.get('parish_id'),
                    'street': values.get('street'),
                    'street2': values.get('street2'),
                    'city': values.get('city'),
                    'zip': values.get('zip'),
                    'ref_point': values.get('ref_point'),
                    'dispatcher_instructions': values.get('dispatcher_instructions'),
                    'relation_us': 'client',
                })

        return self.env.cr.dbname, values.get('login'), values.get('password')
