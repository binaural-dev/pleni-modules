from odoo import models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round
from datetime import datetime, timezone, timedelta

import jwt

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        if self.state in ['sale', 'done']:
            for line in self.order_line:
                line.product_template_id.times_sold += line.product_uom_qty
        return res

    def get_payment_url(self): 
        payload = {
            "user": {
                "id": self.partner_id.id, 
                "name": self.partner_id.name
            },
            "payment": {
                "instantPayment": True,
                "paidElements": [
                    {
                        "id": self.id,
                        "name": self.name,
                        "amount": self.amount_total
                    }
                ],
                "amount": self.amount_total,
                "amountBs": self.amount_total * self.currency_rate,
            },
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24)
        }
        signature = 'swTN5VGPpQjiC7FRDWaDqBVBvNklutZu'
        payment_url = 'https://stag-pay.pleni.app/' + str(
            jwt.encode(payload, signature)
        )

        return payment_url

    def show_payment_methods(self):

        if self.partner_id.property_payment_term_id.id != 1:
            return 'true'

        return 'false'
