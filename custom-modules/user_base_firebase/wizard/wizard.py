# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ReasonCancel(models.TransientModel):
    _name = "push.notification.wizard"
    _inherit = 'user.firebase.message'
    firebase_msg = fields.Many2one('user.firebase.message')
    @api.model
    def action_open_wizard(self):
        objs = self.env['res.partner'].browse(self.env.context.get('active_ids'))
        for obj in objs:
            if not obj.ref_firebase:
                raise ValidationError(_('%s has not allowed permission for push notifications on his/her device.')%obj.name)
        return {
            'name': _('Firebase Notification'),
            'type': 'ir.actions.act_window',
            'res_model': 'push.notification.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': self._context,
        }

    @api.model
    def create(self, values):
        obj = self.env['res.partner'].browse(self.env.context.get('active_ids'))
        values['notification_user_id'] = [(6, 0, obj.ids)]
        obj = self.env['user.firebase.message'].create(values)
        values['firebase_msg'] = obj.id
        return super().create(values)

    def button_submit(self):
        obj = self.firebase_msg
        icon_obj = self.env['ir.attachment'].sudo().search([['res_model', '=', 'user.firebase.message'], ('res_field', '=', 'notification_image'),('res_id', '=', obj.id)])
        if icon_obj:
            icon_obj.public = True
        image_obj = self.env['ir.attachment'].sudo().search([['res_model', '=', 'user.firebase.message'], ('res_field', '=', 'image'), ('res_id', '=', obj.id)])
        if image_obj:
            image_obj.public = True
        notification = {
            'title': obj.title,
            'body': obj.message,
            'icon': obj.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/web/content/' + str(icon_obj.id),
            'action': obj.action_url,
            'button_name': obj.button_active if obj.is_active else 'Open',
            'image': obj.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/web/content/' + str(image_obj.id)
        }
        dict = {}
        if obj.is_device:
            if obj.device_info:
                dict['browser'] = [obj.code for obj in obj.device_info]
            if obj.platform_info:
                dict['platform'] = [obj.code for obj in obj.platform_info]
        obj.env['user.firebase'].send_notification(obj.notification_user_id.ids, notification, dict)
