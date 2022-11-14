from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def write(self, vals):
        res = super(StockPicking, self).write(vals)

        ATC_CHANNEL = 50

        for element in self:
            not_delivered = []
            sale = self.env['sale.order'].search(
                [('name', '=', element.origin)])
            pickings = self.env['sale.order.line'].search(
                [('order_id', '=', sale.id)])

            for p in pickings:
                if p.product_uom_qty > p.qty_to_invoice and p.state == 'sale' and p.invoice_status == 'to invoice':
                    not_delivered.append(p)
                if p.product_uom_qty > p.qty_delivered and p.state == 'sale' and p.invoice_status == 'no':
                    not_delivered.append(p)
                # if p.invoice_status == 'no' and p.state == 'sale' and p.qty_to_invoice != p.product_uom_qty:
                    # not_delivered.append(p)

            if not_delivered:
                ATC_CHANNEL_MSG = {
                    'model': 'mail.channel',
                    'message_type': 'comment',
                    'subtype_id': self.env.ref('mail.mt_comment').id,
                    'channel_ids': [(6, 0, [ATC_CHANNEL])],
                    'body': '<span style="color:red">¡Alerta!</span>' +
                    'La siguiente orden se encuentra con fallas, por favor comunicarsela al cliente: ' +
                    f'<a href="#" data-oe-model="sale.order" data-oe-id="{sale.id}">{sale.name}</a>'
                }
                self.env['mail.message'].create(ATC_CHANNEL_MSG)

        return res
