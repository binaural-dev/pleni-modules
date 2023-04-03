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
        moves = self.env["account.move"].search([('invoice_origin', '=', self.name )])
        print("moveeeeeeeeeeeeeeeeeeeeeeeees", moves)
        payments = []
        total = 0
        totalForeign = 0

        for move in moves:
            _total = move.amount_residual
            if _total == 0:
                print("paso aqui 0")
                return ''
                # raise ValidationError(_("The payment %s is already paid") % move.name)
            _totalForeign = move.amount_residual * move.foreign_currency_id.rate
            print("jjjjjjjjjjjjjjjjjj", move.id, move.name, _total)
            payments.append({"id": move.id, "name": move.name, "amount": _total})

            total += _total
            totalForeign += _totalForeign

        if len(payments) == 0:
            print("paso len aqui 0")
            return ''
            # raise ValidationError(_("There are no payments to pay"))

        payload = {
            "user": {"id": record.partner_id.id, "name": record.partner_id.name},
            "payment": {
                "instantPayment": False,
                "paidElements": payments,
                "amount": total,
                "amountBs": totalForeign,
            },
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24)
        }
        signature = 'swTN5VGPpQjiC7FRDWaDqBVBvNklutZu'
        payment_url = 'https://stag-pay.pleni.app/' + str(
            jwt.encode(payload, signature)
        )

        return payment_url
