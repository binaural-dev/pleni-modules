# -*- coding: utf-8 -*-
from odoo import models


class SaleOrderValidation(models.Model):
    _inherit = 'res.partner'

    def contact_whatsapp(self):
        record_phone = self.mobile
        if not record_phone[0] == '+':
            view = self.env.ref(
                'pleni_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = '¡No hay un código de país! ¡Agregue un número de teléfono válido junto con el código de país!'
            return {
                'name': 'Numero de teléfono inválido',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.errror_message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Whatsapp Message',
                'res_model': 'whatsapp.wizard.contact',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                    'default_template_id': self.env.ref('pleni_whatsapp_integration.whatsapp_contacts_template').id},
            }
