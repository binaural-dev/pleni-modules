# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    type_tax = fields.Selection([('iva', 'IVA'),
                                 ('iva_ret', 'RETENCION IVA'),
                                 ], help="Selecione el Tipo de Impuesto",
                                string="Tipo de Impuesto")
    amount_ret = fields.Float(
        string='Importe de retención',
        digits='Withhold',
        help="Importe de retención de IVA")
    base_ret = fields.Float(
        string='Amount',
        digits='Withhold',
        help="Cantidad sin impuestos")

    @api.model
    def compute_amount_ret(self, invoice):
        """ Calculate withholding amount
        """
        res = {}
        partner = self.env['res.partner']
        acc_part_id = invoice.move_type in ['out_invoice', "out_refund"] and \
                      invoice.company_id.partner_id \
                      or invoice.partner_id
        wh_iva_rate = acc_part_id.wh_iva_rate

        for record in invoice.tax_line:
            amount_ret = 0.0
            if record.tax_id.ret:
                amount_ret = (wh_iva_rate and
                              record.tax_amount * wh_iva_rate / 100.0 or 0.00)
            res[record.id] = {'amount_ret': amount_ret,
                              'base_ret': record.base_amount}
        return res
