from odoo import models, api


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if 'stock_move_id' in val:
                stock_move_id = self.env['stock.move'].search([('id', '=', val['stock_move_id'])])
                if stock_move_id.purchase_line_id and stock_move_id.purchase_line_id.order_id.fixed_rate_boolean:
                    val['currency_bs_rate'] = stock_move_id.purchase_line_id.order_id.fixed_rate
            if 'invoice_origin' in val and val.get('invoice_origin'):
                if val.get('invoice_origin')[0] == 'P':
                    purchase_id = self.env['purchase.order'].search([('name', '=', val['invoice_origin'])])
                    if purchase_id.fixed_rate_boolean:
                        val['currency_bs_rate'] = purchase_id.fixed_rate

        create = super(AccountMoveInherit, self).create(vals_list)

        return create

    @api.onchange('purchase_vendor_bill_id', 'purchase_id')
    def _onchange_purchase_auto_complete(self):
        ''' Load from either an old purchase order, either an old vendor bill.

        When setting a 'purchase.bill.union' in 'purchase_vendor_bill_id':
        * If it's a vendor bill, 'invoice_vendor_bill_id' is set and the loading is done by '_onchange_invoice_vendor_bill'.
        * If it's a purchase order, 'purchase_id' is set and this method will load lines.

        /!\ All this not-stored fields must be empty at the end of this function.
        '''
        if self.purchase_vendor_bill_id.vendor_bill_id:
            self.invoice_vendor_bill_id = self.purchase_vendor_bill_id.vendor_bill_id
            self._onchange_invoice_vendor_bill()
        elif self.purchase_vendor_bill_id.purchase_order_id:
            self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id
            if self.purchase_id.fixed_rate_boolean:
                self.currency_bs_rate = self.purchase_id.fixed_rate

        self.purchase_vendor_bill_id = False

        if not self.purchase_id:
            return

        #A;ado esto para cambiar la tasa


        # Copy data from PO
        invoice_vals = self.purchase_id.with_company(self.purchase_id.company_id)._prepare_invoice()
        invoice_vals['currency_id'] = self.line_ids and self.currency_id or invoice_vals.get('currency_id')
        del invoice_vals['ref']
        self.update(invoice_vals)

        # Copy purchase lines.
        po_lines = self.purchase_id.order_line - self.line_ids.mapped('purchase_line_id')
        new_lines = self.env['account.move.line']
        for line in po_lines.filtered(lambda l: not l.display_type):
            new_line = new_lines.new(line._prepare_account_move_line(self))
            new_line.account_id = new_line._get_computed_account()
            new_line._onchange_price_subtotal()
            new_lines += new_line
        new_lines._onchange_mark_recompute_taxes()

        # Compute invoice_origin.
        origins = set(self.line_ids.mapped('purchase_line_id.order_id.name'))
        self.invoice_origin = ','.join(list(origins))

        # Compute ref.
        refs = self._get_invoice_reference()
        self.ref = ', '.join(refs)

        # Compute payment_reference.
        if len(refs) == 1:
            self.payment_reference = refs[0]

        self.purchase_id = False
        self._onchange_currency()
        self.partner_bank_id = self.bank_partner_id.bank_ids and self.bank_partner_id.bank_ids[0]
