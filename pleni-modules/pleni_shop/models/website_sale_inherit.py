from datetime import datetime

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers.portal import PaymentProcessing

class WebsiteSaleController(WebsiteSale):
    @http.route(['/shop/payment/transaction/',
        '/shop/payment/transaction/<int:so_id>',
        '/shop/payment/transaction/<int:so_id>/<string:access_token>'], type='json', auth="public", website=True)
    def payment_transaction(self, acquirer_id, delivery_date=None, delivery_hour=None ,client_notes='', save_token=False, so_id=None, access_token=None, token=None, **kwargs):
        """ Json method that creates a payment.transaction, used to create a
        transaction when the user clicks on 'pay now' button. After having
        created the transaction, the event continues and the user is redirected
        to the acquirer website.

        :param int acquirer_id: id of a payment.acquirer record. If not set the
                                user is redirected to the checkout page
        """

        # convertir el string en fecha
        if delivery_date:
            new_delivery_date = datetime.strptime(delivery_date, '%Y-%m-%d')

        # Ensure a payment acquirer is selected
        if not acquirer_id:
            return False

        try:
            acquirer_id = int(acquirer_id)
        except:
            return False

        # Retrieve the sale order
        if so_id:
            env = request.env['sale.order']
            domain = [('id', '=', so_id)]
            if access_token:
                env = env.sudo()
                domain.append(('access_token', '=', access_token))
            order = env.search(domain, limit=1)
        else:
            order = request.website.sale_get_order()

        # Ensure there is something to proceed
        if not order or (order and not order.order_line):
            return False

        assert order.partner_id.id != request.website.partner_id.id

        # Create transaction
        vals = {'acquirer_id': acquirer_id,
                'return_url': '/shop/payment/validate'}

        if save_token:
            vals['type'] = 'form_save'
        if token:
            vals['payment_token_id'] = int(token)

        transaction = order._create_payment_transaction(vals)

        if delivery_date:
            order.update({
                'date_delivery_view': new_delivery_date, # fecha de delivery
                'expected_date': new_delivery_date
            })

        if client_notes:
            order.update({
                'client_notes': client_notes # notas del cliente
            })

        if delivery_hour:
            order.update({
                'am_pm': delivery_hour
            })

        salesman_id = request.env['res.partner'].browse(order.partner_id.id).salesman_id.id
        if salesman_id:
            order.update({
                'salesman_id': salesman_id
            })
        # store the new transaction into the transaction list and if there's an old one, we remove it
        # until the day the ecommerce supports multiple orders at the same time
        last_tx_id = request.session.get('__website_sale_last_tx_id')
        last_tx = request.env['payment.transaction'].browse(last_tx_id).sudo().exists()
        if last_tx:
            PaymentProcessing.remove_payment_transaction(last_tx)
        PaymentProcessing.add_payment_transaction(transaction)
        request.session['__website_sale_last_tx_id'] = transaction.id

        order.write({'payment_methods': [(4, acquirer_id)] })

        if delivery_date and delivery_hour:
            commitment_date = self.get_commitment_date_format(order.date_delivery_view, order.am_pm)
            order.update({
                'commitment_date': commitment_date
            })
        return transaction.render_sale_button(order)

    def get_commitment_date_format(self, date_delivery_view, am_pm, partner_id):
        if date_delivery_view and am_pm:
            # 8 + 4 System hour
            hour = 12 + 4 if am_pm == 'am' else 5 + 4
            return datetime(
                date_delivery_view.year, 
                date_delivery_view.month,
                date_delivery_view.day,
                hour,0,0 
            )

        return False

    def get_partner_hours(self, partner_id, delivery_date, am_pm):
        partner = request.env['res.partner'].browse(partner_id)
        day = delivery_date.strftime("%A")

        days_open = {
            'Monday': partner.monday_open,
            'Tuesday': partner.tuesday_open,
            'Wednesday': partner.wednesday_open,
            'Thursday': partner.thursday_open,
            'Friday': partner.friday_open,
            'Saturday': partner.saturday_open,
            'Sunday': partner.sunday_open
        }

        days_from = {
            'Monday': partner.monday_from,
            'Tuesday': partner.tuesday_from,
            'Wednesday': partner.wednesday_from,
            'Thursday': partner.thursday_from,
            'Friday': partner.friday_from,
            'Saturday': partner.saturday_from,
            'Sunday': partner.sunday_from
        }

        days_to = {
            'Monday': partner.monday_to,
            'Tuesday': partner.tuesday_to,
            'Wednesday': partner.wednesday_to,
            'Thursday': partner.thursday_to,
            'Friday': partner.friday_to,
            'Saturday': partner.saturday_to,
            'Sunday': partner.sunday_to
        }

        if days_open[day]:
            if am_pm == 'am':
                time = datetime.strptime(days_from[day], '%H:%M')
                if 8 <= time.hour <= 12:
                    return datetime(
                        date_delivery_view.year, 
                        date_delivery_view.month,
                        date_delivery_view.day,
                        time.hour,0,0 
                    )

        
        if day == 'Monday' and partner.monday_open:

            return f'Lunes: {self.monday_from}-{self.monday_to}'

        if day == 'Tuesday' and partner.tuesday_open:
            return f'Martes: {self.tuesday_from}-{self.tuesday_to}'
        
        if day == 'Wednesday' and partner.wednesday_open:
            return f'Miércoles: {self.wednesday_from}-{self.wednesday_to}'
                
        if day == 'Thursday' and partner.thursday_open:
            return f'Jueves: {self.thursday_from}-{self.thursday_to}'

        if day == 'Friday' and partner.friday_open:
            return f'Viernes: {self.friday_from}-{self.friday_to}'

        if day == 'Saturday' and partner.saturday_open:
            return f'Sábado: {self.saturday_from}-{self.saturday_to}'

        if day == 'Sunday' and partner.sunday_open:
            return f'Domingo: {self.sunday_from}-{self.sunday_to}'
        
        return False
