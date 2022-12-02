# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-Today Geminate Consultancy Services (<http://geminatecs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import http, _, tools
import json
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

CustomerPortal.OPTIONAL_BILLING_FIELDS += ['register_all_notification']

class UserBaseFirebase(http.Controller):

    @http.route('/user_base_firebase/set_firebase_data', auth='public', type='http', csrf=False)
    def set_firebase_data(self, token, ** kw):
        Firebase = request.env['user.firebase'].sudo()
        obj = Firebase.search([['token', '=', token]],limit=1,order='id desc')
        if not obj:
            obj = Firebase.search([['ref_partner','=',request.env.user.partner_id.id],['browser','=',request.httprequest.user_agent.browser],['ip','=',request.httprequest.remote_addr],['platform','=',request.httprequest.user_agent.platform]],limit=1,order='id desc')

        values = {'token': token, 'ref_partner': request.env.user.partner_id.id, 'browser': request.httprequest.user_agent.browser, 'ip': request.httprequest.remote_addr,
                  'port': request.httprequest.environ['REMOTE_PORT'], 'platform': request.httprequest.user_agent.platform, 'version': request.httprequest.user_agent.version, 'string': request.httprequest.user_agent.string,'isactive':True}

        brow_obj = request.env['user.firebase.browser'].sudo().search([['code', '=', values['browser']]])
        if not brow_obj:
            brow_obj.create({'code': values['browser']})
        platform_obj = request.env['user.firebase.platform'].sudo().search([['code', '=', values['platform']]])
        if not platform_obj:
            platform_obj.create({'code': values['platform']})

        if not obj:
            obj = Firebase.create(values)
        else:
            obj.write(values)
        request.session['user_wise_token'] = str(obj.id)
        return ''

    @http.route('/user_base_firebase/get_firebase_data', auth='public', type='http', csrf=False)
    def get_firebase_data(self,** kw):
        firebase_data = {
            'apiKey': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.apiKey'),
            'authDomain': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.authDomain'),
            'databaseURL': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.databaseURL'),
            'projectId': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.projectId'),
            'storageBucket': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.storageBucket'),
            'messagingSenderId': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.messagingSenderId'),
            'appId': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.appId'),
            'measurementId': request.env['ir.config_parameter'].sudo().get_param('user_base_firebase.measurementId')
        }
        return json.dumps(firebase_data)


class CustomerPortalInherit(CustomerPortal):

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        if post and request.httprequest.method == 'POST' and request.session.get('user_wise_token'):
            request.env['user.firebase'].sudo().browse(int(request.session.get('user_wise_token'))).isactive =  True if post.get('register_specific_notification') else False
            if not post.get('register_all_notification'):
                request.env.user.partner_id.register_all_notification = 'false'
        return super(CustomerPortalInherit, self).account(redirect,**post)

    def details_form_validate(self, data):
        self.OPTIONAL_BILLING_FIELDS.append('register_specific_notification')
        error, error_message = super(CustomerPortalInherit, self).details_form_validate(data)
        self.OPTIONAL_BILLING_FIELDS.remove('register_specific_notification')
        return error, error_message
