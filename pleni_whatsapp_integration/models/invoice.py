from odoo import models, _
from odoo.exceptions import UserError

from itertools import groupby
import urllib.parse as parse


class InvoiceTransferDone(models.Model):
    _inherit = 'account.move'

    def invoice_whatsapp(self):
        record_phone = self.partner_id.mobile
        if not record_phone:
            view = self.env.ref(
                'pleni_whatsapp_integration.warn_message_wizard')
            view_id = view and view.id or False
            context = dict(self._context or {})
            context['message'] = 'El cliente no tiene número de teléfono'
            return {
                'name': 'Sin número de teléfono',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
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
                'res_model': 'display.error.message',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context
            }
        else:
            self.message_post(type="notification", body=_(self.state))
            return {
                'type': 'ir.actions.act_window',
                'name': 'Whatsapp Message',
                'res_model': 'whatsapp.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {
                    'default_template_id': self.env.ref('pleni_whatsapp_integration.whatsapp_invoice_template').id},
            }

    def send_direct_message(self):
        record_phone = self.partner_id.mobile
        products = ""
        for record in self:
            for id in record.invoice_line_ids:
                products = products + "*" + \
                    str(id.product_id.name) + " : " + str(id.quantity) + "* \n"

        custom_msg = "Hola *{}*, tu Nota de Entrega *{}* con el monto de *{} {}* está lista.\nLa Nota de Entrega contiene los siguientes items: \n{}".format(
            str(self.partner_id.name), str(self.name), str(self.currency_id.symbol), str(self.amount_total), products)
        phone_number = [
            number for number in record_phone if number.isnumeric()]
        phone_number = "".join(phone_number)
        phone_number = "+" + phone_number

        link = 'https://web.whatsapp.com/send?phone=' + phone_number
        message_string = parse.quote(custom_msg)

        url = link + "&text=" + message_string
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'res_id': self.id,
        }

    def check_value(self, partner_ids):
        partners = groupby(partner_ids)
        return next(partners, True) and not next(partners, False)

    def multi_sms(self):
        invoice_order_ids = self.env['account.move'].browse(
            self.env.context.get('active_ids'))

        customer_ids = []
        invoice_nums = []
        for sale in invoice_order_ids:
            customer_ids.append(sale.partner_id.id)
            invoice_nums.append(sale.name)

        # To check unique customers
        customer_check = self.check_value(customer_ids)

        if customer_check:
            invoice_numbers = invoice_order_ids.mapped('name')
            invoice_numbers = "\n".join(invoice_numbers)

            form_id = self.env.ref(
                'pleni_whatsapp_integration.whatsapp_multiple_message_wizard_form').id
            product_all = []
            for each in invoice_order_ids:
                products = ""
                for id in each.move_line_ids_without_package:
                    products = products + "*" + "Producto: " + \
                        str(id.product_id.name) + ", Cantidad: " + \
                        str(id.quantity) + "* \n"
                product_all.append(products)

            custom_msg = "Hola *{}*,\nTus Notas de Entrega\n{} \n están listas para su revisión.\n".format(
                str(self.partner_id.name), invoice_numbers
            )

            counter = 0
            for every in product_all:
                custom_msg = custom_msg + "Tu orden *{}* contiene los siguientes items: \n{}\n".format(
                    invoice_nums[counter], every
                )
                counter += 1

            final_msg = custom_msg + \
                "\n No dude en ponerse en contacto con nosotros si tiene alguna pregunta."

            context = dict(self.env.context)
            context.update({
                'default_message': final_msg,
                'default_partner_id': self.partner_id.id,
                'default_mobile': self.partner_id.mobile,
            })
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'whatsapp.wizard.multiple.contact',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': context,
            }
        else:
            raise UserError('Seleccione pedidos de clientes únicos')
