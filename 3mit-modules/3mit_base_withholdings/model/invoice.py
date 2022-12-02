# coding: utf-8
###########################################################################
import time
from odoo import api,fields,models
from odoo.exceptions import UserError
from odoo.fields import _
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def ret_and_reconcile(self, pay_amount, pay_account_id,
                          pay_journal_id, writeoff_acc_id,
                          writeoff_journal_id, date,
                          name, to_wh,type_retencion):
        """ Make the payment of the invoice
        """

        rp_obj = self.env['res.partner']
        hola = self.ids
        carro = hola
        if self.ids :
            assert len(self.ids) == 1, "Solo puede pagar una factura a la vez"
        else:
            assert len(to_wh) == 1, "Solo puede pagar una factura a la vez"
        invoice = self.browse(self.ids)
        src_account_id = pay_account_id.id
        fecha_tasa = date
        fecha_tasa = fields.datetime.combine(fecha_tasa, fields.datetime.max.time())
        currency_bs_rate = self.env['res.currency.rate'].search(
            [('currency_id', '=', 2), ('name', '<=', fecha_tasa)],
            order='id desc', limit=1).rate_divided

        move = {'ref': name + 'de ' + str(invoice.name),
                'journal_id': pay_journal_id,
                'date': date,
                'state': 'draft',
                'type_name': 'entry',
                'currency_id': self.env.company.currency_id.id,
                'currency_bs_rate': currency_bs_rate

                }
        if currency_bs_rate != 0 and currency_bs_rate != 1:
            move['currency_bs_rate'] = currency_bs_rate

        move_obj = self.env['account.move']
        move_id = move_obj.create(move)
        move_id.currency_bs_rate = currency_bs_rate
        # Take the seq as name for move

        types = {'out_invoice': -1,
                 'in_invoice': 1,
                 'out_refund': 1, 'in_refund': -1}
        direction = types[invoice.move_type]

        if type_retencion != 'wh_islr':
            l1 = {
                'account_id': src_account_id,
                'currency_id': self.env.company.currency_id.id,
                'ref': invoice.name,
                'date': date,
                'partner_id': rp_obj._find_accounting_partner(invoice.partner_id).id,
                'move_id': move_id.id,
                'name': name,
                'debit': direction * pay_amount > 0 and direction * pay_amount,
                'credit': direction * pay_amount < 0 and - direction * pay_amount,
                'amount_currency': direction * pay_amount,
            }
        else:
            if invoice.move_type in ["out_invoice", "in_invoice"]:
                l1 = {
                    'account_id': src_account_id,
                    'currency_id': self.env.company.currency_id.id,
                    'ref': invoice.name,
                    'date': date,
                    'partner_id': rp_obj._find_accounting_partner(invoice.partner_id).id,
                    'move_id': move_id.id,
                    'name': name,
                    'debit': abs(pay_amount),
                    'credit': False,
                    'amount_currency': abs(pay_amount),
                }
            else:
                l1 = {
                    'account_id': src_account_id,
                    'currency_id': self.env.company.currency_id.id,
                    'ref': invoice.name,
                    'date': date,
                    'partner_id': rp_obj._find_accounting_partner(invoice.partner_id).id,
                    'move_id': move_id.id,
                    'name': name,
                    'debit': False,
                    'credit': abs(pay_amount),
                    'amount_currency': - abs(pay_amount),
                }

        move_line_obj = self.env['account.move.line']
        move_line_id1 = move_line_obj.with_context(check_move_validity=False).create(l1)

        if type_retencion == 'wh_iva':
            l2 = self._get_move_lines1(to_wh, pay_journal_id, writeoff_acc_id,
                                      writeoff_journal_id, date, name)
        if type_retencion == 'wh_muni':
            l2 = self._get_move_lines3(to_wh, pay_journal_id, writeoff_acc_id,
                                      writeoff_journal_id, date, name)

        if type_retencion != 'wh_islr':
            if not l2:
                raise UserError("Advertencia! \nNo se crearon movimientos contables.\n Por favor, verifique si hay impuestos / conceptos para retener en las facturas!")

        #Acumular todos los elementos de l2 en una sola línea
        if type_retencion == 'wh_islr':
            acc = invoice.islr_wh_doc_id.journal_id.default_islr_account.id
            acc_part_id = rp_obj._find_accounting_partner(invoice.islr_wh_doc_id.partner_id)
            if not acc:
                raise UserError(
                    "Falta la cuenta en el impuesto! \nEl diario de [%s] tiene las cuentas faltantes. Por favor, rellene los campos que faltan para poder continuar" % (
                        invoice.islr_wh_doc_id.journal_id.name))

            if invoice.move_type in ["out_invoice", "in_invoice"]:
                l2 = {
                    'amount_currency': - abs(l1["amount_currency"]),
                    'debit': False,
                    'credit': l1["debit"],
                    'account_id': acc,
                    'partner_id': acc_part_id.id,
                    'ref': self.display_name,
                    'date': date,
                    'currency_id': self.env.company.currency_id.id,
                    'name': name.strip() + ' - ISLR: ' + invoice.islr_wh_doc_id.name.strip()
                }
            else:
                l2 = {
                    'amount_currency': abs(l1["amount_currency"]),
                    'debit': l1["credit"],
                    'credit': False,
                    'account_id': acc,
                    'partner_id': acc_part_id.id,
                    'ref': self.display_name,
                    'date': date,
                    'currency_id': self.env.company.currency_id.id,
                    'name': name.strip() + ' - ISLR: ' + invoice.islr_wh_doc_id.name.strip()
                    }

            l2["move_id"] = move_id.id

            move_line_obj.with_context(check_move_validity=False).create(l2)
        else:
            deb = l2[0][2]['debit']
            cred = l2[0][2]['credit']
            if deb < 0: l2[0][2].update({'debit': deb * direction})
            if cred < 0: l2[0][2].update({'credit': cred * direction})
            l2 = l2[0][2]
            l2['move_id'] = move_id.id
            move_line_id2 = move_line_obj.create(l2)

        return move_id

        line_ids = []
        total = 0.0
        line = self.env['account.move.line']
        self._cr.execute(
            'select id'
            ' from account_move_line'
            ' where move_id in (' + str(move_id.id) + ',' +
            str(invoice.move_id.id) + ')')
        lines = line.browse( [item[0] for item in self._cr.fetchall()])
        for aml_brw in lines:
            if aml_brw.account_id.id == src_account_id:
                line_ids.append(aml_brw.id)
                total += (aml_brw.debit or 0.0) - (aml_brw.credit or 0.0)
        for aml_brw in invoice.payment_ids:
            if aml_brw.account_id.id == src_account_id:
                line_ids.append(aml_brw.id)
                total += (aml_brw.debit or 0.0) - (aml_brw.credit or 0.0)
        if (not round(total, self.env['decimal.precision'].precision_get(
                 'Withhold'))) or writeoff_acc_id:
            self.env['account.move.line'].reconcile(
                 line_ids, 'manual', writeoff_acc_id,
                writeoff_period_id, writeoff_journal_id)

        self.env['account.move'].write({})
        self.move_id = move_id


    def _get_move_lines(self, to_wh,
                        pay_journal_id, writeoff_acc_id,
                        writeoff_journal_id, date, name
                        ):
        """ Function openerp is rewritten for adaptation in
        the ovl
        """
        return []

    def ret_payment_get(self,*args):
        """ Return payments associated with this bill
        """
        # /!\ This method need revision and I (hbto) have come to believe it is
        # useless at worst, at best it needs to be refactored, to get payments
        # from invoice one just need to look at the payment_ids field
        lines = []
        return lines

class AccountInvoiceTax(models.Model):
    _inherit = 'account.tax'

    tax_id = fields.Many2one(
            'account.tax', 'Tax', required=False, ondelete='set null',
            help="Tax relation to original tax, to be able to take off all"
                 " data from invoices.", )

    @api.model
    def compute(self, invoice):
        """ Calculate the amount, base, tax amount,
        base amount of the invoice
        """
        tax_grouped = {}
        if isinstance(invoice, (int)):
            inv = self.env['account.move'].browse(invoice)
        else:
            inv = invoice
        currency = inv.currency_id.with_context(
            date=inv.date_invoice or time.strftime('%Y-%m-%d'))
        company_currency = inv.company_id.currency_id
        for line in inv.invoice_line:
            for tax in line.invoice_line_tax_id.compute_all(
                    (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                    line.quantity, line.product_id, inv.partner_id)['taxes']:
                val = {}
                val['invoice_id'] = inv.id
                val['name'] = tax['name']
                val['amount'] = tax['amount']
                val['manual'] = False
                val['sequence'] = tax['sequence']
                val['base'] = tax['price_unit'] * line['quantity']
                # add tax id #
                val['tax_id'] = tax['id']

                if inv.type_name in ('out_invoice', 'in_invoice'):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute(
                        val['base'] * tax['base_sign'], company_currency,
                        round=False)
                    val['tax_amount'] = currency.compute(
                        val['amount'] * tax['tax_sign'], company_currency,
                        round=False)
                    val['account_id'] = tax['account_collected_id'] or \
                                        line.account_id.id
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute(
                        val['base'] * tax['ref_base_sign'], company_currency,
                        round=False)
                    val['tax_amount'] = currency.compute(
                        val['amount'] * tax['ref_tax_sign'], company_currency,
                        round=False)
                    val['account_id'] = tax['account_paid_id'] or \
                                        line.account_id.id

                key = (val['tax_id'])
                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for tax in tax_grouped.values():
            tax['base'] = currency.round(tax['base'])
            tax['amount'] = currency.round(tax['amount'])
            tax['base_amount'] = currency.round(tax['base_amount'])
            tax['tax_amount'] = currency.round(tax['tax_amount'])
        return tax_grouped