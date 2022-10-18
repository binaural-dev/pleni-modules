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
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests
import ast
import json
from odoo.http import request
import requests

def send_firebase_notification(serverToken, tokens, notification):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }
    for token in tokens:
        body = {
            'notification': notification,
            'to': token,
            'priority': 'high',
            'data': notification,
        }
        print("data1", body)
        print("data2", json.dumps(body))
        try:
            requests.post("https://fcm.googleapis.com/fcm/send",headers=headers, data=json.dumps(body))
        except Exception:
            pass

class UserFirebaseMeaage(models.Model):
    _name = 'user.firebase.message'
    _description = "Firebase Message"

    message = fields.Text('Message', help='Message displayed in notification.', required=True)
    title = fields.Text('Title', help='Title displayed in notification.', required=True)
    notification_image = fields.Binary('Icon', required=True)
    action_url = fields.Text(string="URL", required=True)
    image = fields.Binary(string='Image', required=True)
    is_device = fields.Boolean(string="Is Device")
    is_active = fields.Boolean(string="Is Actiive")
    button_active = fields.Char(string="Button Name")
    notification_user_id = fields.Many2many("res.partner", string="User")
    device_info = fields.Many2many('user.firebase.browser', string='Device Info')
    platform_info = fields.Many2many('user.firebase.platform', string='Platform Info')


class FirebaseModel(models.Model):
    _name = 'user.firebase'

    ip = fields.Char('Ip address From User')
    browser = fields.Char('Browser_name')
    port = fields.Char()
    platform = fields.Char()
    version = fields.Char()
    token = fields.Text()
    string = fields.Text()
    ref_partner = fields.Many2one(
        'res.partner', string='Partner from Contacts')
    isactive = fields.Boolean(default=True)

    def send_notification(self, partner_ids, notification,*args):
        args = args[0]
        partners = self.env['res.partner'].sudo().search([['id','in',partner_ids],['register_all_notification','=','true']])
        domain = [['ref_partner', 'in', partners.ids],['isactive','=',True]]
        if args.get('platform'):
            domain.append(['platform','in',args.get('platform')])
        if args.get('browser'):
            domain.append(['browser','in',args.get('browser')])
        objs = self.sudo().search(domain)
        if objs:
            serverToken = self.env['ir.config_parameter'].sudo().get_param(
                'user_base_firebase.serverToken')
            if serverToken:
                tokens = [obj.token for obj in objs if obj.token]
                send_firebase_notification(serverToken, tokens, notification)


class BrowserInfo(models.Model):
    _name = "user.firebase.browser"
    name = fields.Char()
    code = fields.Char()

    @api.model
    def create(self, vals):
        if vals.get('code'):
            vals['name'] = vals.get('code').capitalize()
        result = super(BrowserInfo, self).create(vals)
        return result

class PlatformInfo(models.Model):
    _name = "user.firebase.platform"
    name = fields.Char()
    code = fields.Char()

    @api.model
    def create(self, vals):
        if vals.get('code'):
            vals['name'] = vals.get('code').capitalize()
        result = super(PlatformInfo, self).create(vals)
        return result

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    register_all_notification = fields.Char(default='true')
    ref_firebase = fields.One2many(
        'user.firebase', 'ref_partner', string='Website Seller Price')

    def append_firebase(self,post):
        if post.get('register_notification'):
            if self.ref_firebase:
                objs = self.env['user.firebase'].search(
                    [['id', 'in', self.ref_firebase.ids], ['browser', '=', post['browser']], ['platform', '=', post['platform']], ['token', '=', post['firebase_token']]])
                brow_obj = self.env['user.firebase.browser'].sudo().search([['code','=',post['browser']]])
                if not brow_obj:
                    brow_obj.create({'code': post['browser']})

                platform_obj = self.env['user.firebase.platform'].sudo().search([['code','=',post['platform']]])
                if not platform_obj:
                    platform_obj.create({'code': post['platform']})

                if objs:
                    return True
            self.create_firebase_obj(post)

    def create_firebase_obj(self,post):
        values = {key: post.get(key)
                  for key in ['ip', 'browser', 'platform', 'version', 'port', 'string']}
        brow_obj = self.env['user.firebase.browser'].sudo().search([['code', '=', post['browser']]])
        if not brow_obj:
            brow_obj.create({'code': post['browser']})

        platform_obj = self.env['user.firebase.platform'].sudo().search([['code', '=', post['platform']]])
        if not platform_obj:
            platform_obj.create({'code': post['platform']})

        values.update(
            {'ref_partner': self.id, 'token': post.get('firebase_token')})
        self.env['user.firebase'].create(values)

    def check_specific_firebase(self):
        domain = [['ref_partner','=',request.env.user.partner_id.id],['browser','=',request.httprequest.user_agent.browser],['platform','=',request.httprequest.user_agent.platform]]
        if request.session.get('user_wise_token'):
            domain.append(['id','=',int(request.session.get('user_wise_token'))])
        obj = request.env['user.firebase'].search(domain,limit=1,order='id desc')
        if obj and obj.isactive:
            return 'true'
        else:
            return 'false'

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    user_wise_notification_apiKey = fields.Char("Firebase ApiKey")
    user_wise_notification_authDomain = fields.Char(
        "Firebase AuthDomain")
    user_wise_notification_databaseURL = fields.Char(
        "Firebase DatabaseURL")
    user_wise_notification_projectId = fields.Char(
        "Firebase ProjectId")
    user_wise_notification_storageBucket = fields.Char(
        "Firebase StorageBucket")
    user_wise_notification_messagingSenderId = fields.Char(
        "Firebase MessagingSenderId")
    user_wise_notification_appId = fields.Char(
        "Firebase AppId")
    user_wise_notification_measurementId = fields.Char(
        "Firebase MeasurementId")
    user_wise_notification_serverToken = fields.Char(
        "Firebase ServerToken")

    @api.model
    def get_values(self):
        config_parameter_obj_sudo = self.env["ir.config_parameter"].sudo()
        res = super(ResConfigSettings, self).get_values()
        res["user_wise_notification_apiKey"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.apiKey"
        )
        res["user_wise_notification_authDomain"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.authDomain"
        )
        res["user_wise_notification_databaseURL"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.databaseURL"
        )
        res["user_wise_notification_projectId"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.projectId"
        )
        res["user_wise_notification_storageBucket"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.storageBucket"
        )
        res["user_wise_notification_messagingSenderId"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.messagingSenderId"
        )
        res["user_wise_notification_appId"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.appId"
        )
        res["user_wise_notification_measurementId"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.measurementId"
        )
        res["user_wise_notification_serverToken"] = config_parameter_obj_sudo.get_param(
            "user_base_firebase.serverToken"
        )
        return res

    @api.model
    def set_values(self):
        config_parameter_obj_sudo = self.env["ir.config_parameter"].sudo()
        res = super(ResConfigSettings, self).set_values()
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.apiKey", self.user_wise_notification_apiKey)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.authDomain", self.user_wise_notification_authDomain)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.databaseURL", self.user_wise_notification_databaseURL)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.projectId", self.user_wise_notification_projectId)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.storageBucket", self.user_wise_notification_storageBucket)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.messagingSenderId", self.user_wise_notification_messagingSenderId)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.appId", self.user_wise_notification_appId)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.measurementId", self.user_wise_notification_measurementId)
        config_parameter_obj_sudo.set_param(
            "user_base_firebase.serverToken", self.user_wise_notification_serverToken)
