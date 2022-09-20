# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    rela_wh_iva = fields.Many2one('account.wh.iva')

    wh_iva = fields.Boolean('¿Ya se ha retenido esta factura con el IVA?',
                            copy=False, help="Los movimientos de la cuenta de la factura han sido retenidos con "
                                             "movimientos de cuenta de los pagos.")
    wh_iva_id = fields.Many2one(
        'account.wh.iva', string='Documento de Retención de IVA',
        compute='_compute_wh_iva_id', store=True,
        help="Este es el documento de retención de IVA donde en esta factura "
             "está siendo retenida.")
    vat_apply = fields.Boolean(
        string='Excluir este documento de la retención del IVA',
        states={'draft': [('readonly', False)]},
        help="Esta selección indica si generar la factura "
             "documento de retención")

    @api.depends('wh_iva_id.wh_lines')
    def _compute_wh_iva_id(self):
        for record in self:
            lines = self.env['account.wh.iva.line'].search([
                ('invoice_id', '=', record.id)])
            record.wh_iva_id = lines and lines[0].retention_id.id or False

    def already_posted_iva(self):
        amount_tax = 0
        result = None
        if self:
            result = self._compute_wh_iva_id()
            for inv in self.line_ids:
                if len(self.line_ids.tax_ids) == 1:
                    for tax in inv.tax_ids:
                        if tax.amount == 0:
                            amount_tax = 2000
        if self.company_id.partner_id.wh_iva_agent and self.partner_id.wh_iva_agent and result and amount_tax == 0:
            if self.state == 'posted':
                self.check_document_date()
                self.check_invoice_dates()
                apply = self.check_wh_apply()
                if apply:
                    self.check_withholdable()
                    self.action_wh_iva_supervisor()
                    self.action_wh_iva_create()

    def attach_iva_to_credit_note(self):
        amount_tax = 0
        result = None
        for i in self:
            if i:
                result = i._withholdable_tax()
                for inv in i.line_ids:
                    if len(i.line_ids.tax_ids) == 1:
                        for tax in inv.tax_ids:
                            if tax.amount == 0:
                                amount_tax = 2000
            if i.company_id.partner_id.wh_iva_agent and i.partner_id.wh_iva_agent and result and amount_tax == 0:
                if i.state == 'posted':
                    i.check_document_date()
                    i.check_invoice_dates()
                    apply = i.check_wh_apply()
                    if apply:
                        i.check_withholdable()
                        i.action_wh_iva_supervisor()
                        i.action_wh_iva_create()

    def action_post(self):
        var = super(AccountMove, self).action_post()
        amount_tax = 0
        result = None
        for i in self:
            if i:
                result = i._withholdable_tax()
                for inv in i.line_ids:
                    if len(i.line_ids.tax_ids) == 1:
                        for tax in inv.tax_ids:
                            if tax.amount == 0:
                                amount_tax = 2000
            if i.company_id.partner_id.wh_iva_agent and i.partner_id.wh_iva_agent and result and amount_tax == 0:
                if i.state == 'posted':
                    i.check_document_date()
                    i.check_invoice_dates()
                    apply = i.check_wh_apply()
                    if apply:
                        i.check_withholdable()
                        i.action_wh_iva_supervisor()
                        i.action_wh_iva_create()
        return var

    def check_document_date(self):
        """
        check that the invoice in open state have the document date defined.
        @return True or raise an orm exception.
        """
        for inv_brw in self:
            if (inv_brw.move_type in ('in_invoice', 'in_refund', 'out_invoice', 'out_refund') and
                    inv_brw.state == 'posted' and not inv_brw.date):
                raise UserError(
                    "Advertencia \nLa fecha del documento no puede estar vacía cuando la factura se encuentra en "
                    "estado publicado.")
        return True

    def check_invoice_dates(self):
        """
        check that the date document is less or equal than the date invoice.
        @return True or raise and osv exception.
        """
        for inv_brw in self:
            if (inv_brw.move_type in ('in_invoice', 'in_refund', 'out_invoice', 'out_refund') and
                    inv_brw.date and not inv_brw.invoice_date <= inv_brw.date):
                raise UserError("Warning \nThe document date must be less or equal than the invoice date.")
        return True

    def wh_iva_line_create(self):
        """ Creates line with iva withholding
        """
        wil_obj = self.env['account.wh.iva.line']
        partner = self.env['res.partner']
        values = {}
        type_invoice = ''
        for inv_brw in self:
            wh_iva_rate = (
                    inv_brw.move_type in ('in_invoice', 'in_refund', 'out_refund', 'out_invoice') and
                    inv_brw.partner_id.wh_iva_rate or
                    inv_brw.company_id.partner_id.wh_iva_rate)
            if inv_brw.move_type in ('in_invoice', 'out_invoice', 'out_refund', 'in_refund'):
                if inv_brw.debit_origin_id and inv_brw.move_type == 'out_invoice':
                    type_invoice = 'out_debit'
                elif inv_brw.move_type == 'in_invoice' and inv_brw.debit_origin_id:
                    type_invoice = 'in_debit'
                elif not inv_brw.debit_origin_id and inv_brw.move_type in (
                        'out_invoice', 'in_invoice', 'in_refund', 'out_refund'):
                    type_invoice = inv_brw.move_type

            values = {'name': _('IVA WH - ORIGIN %s' % inv_brw.name),
                      'invoice_id': inv_brw.id,
                      'wh_iva_rate': wh_iva_rate,
                      'type': type_invoice,
                      }
        return values and wil_obj.create(values)

    def action_wh_iva_supervisor(self):
        """ Validate the currencys are equal
        """
        for inv in self:
            if inv.amount_total == 0.0:
                raise UserError(
                    f"Acción Invalida! Esta factura tiene una cantidad total {inv.amount_total} {inv.currency_id.symbol} verifique el precio de los productos.")
        return True

    def get_fortnight_wh_id(self):
        """ Returns the id of the acc.wh.iva in draft state that correspond to
        the invoice fortnight. If not exist return False.
        """
        wh_iva_obj = self.env['account.wh.iva']
        for inv_brw in self:
            acc_part_id = inv_brw.partner_id
            type_move = (inv_brw.move_type in ["in_refund", "out_refund"])
            for wh_iva in wh_iva_obj.search([
                ('state', '=', 'draft'), ('type', '=', type_move), '|',
                ('partner_id', '=', acc_part_id.id),
                ('partner_id', 'child_of', acc_part_id.id)]):
                return wh_iva.id
        return False

    def action_wh_iva_create(self):
        """ Create withholding objects """
        ret_iva = []
        for inv in self:
            if inv.wh_iva_id:
                if inv.wh_iva_id.state == 'draft':
                    pass
                else:
                    raise UserError(_('Ya tiene un documento de retención asociado a su factura, pero este documento '
                                      'de retención no está en cancelar estado.'))
            else:
                # Create Lines Data
                ret_id = {}
                journal = 0
                acc_id = 0
                ret_line_id = inv.wh_iva_line_create()
                # Create a New WH Doc and add line
                type_invoice = ''
                wh_iva_obj = self.env['account.wh.iva']
                rp_obj = self.env['res.partner']
                values = {}
                for inv_brw in self:
                    acc_part_id = inv_brw.partner_id
                    if inv_brw.move_type in ('out_invoice', 'out_refund', '_out_debit'):
                        acc_id = acc_part_id.property_account_receivable_id.id
                    elif inv_brw.move_type in ('in_invoice', 'in_refund', '_in_debit'):
                        acc_id = acc_part_id.property_account_payable_id.id
                    if inv_brw.move_type in ('out_invoice', 'out_refund'):
                        if inv_brw.debit_origin_id and inv_brw.move_type == 'out_invoice':
                            type_invoice = 'out_debit'
                            journal = acc_part_id.purchase_sales_id.id
                        elif not inv_brw.debit_origin_id and inv_brw.move_type in ('out_invoice', 'out_refund'):
                            type_invoice = inv_brw.move_type
                            journal = acc_part_id.purchase_sales_id.id
                        values = {'name': _('IVA WH CLIENTE - ORIGIN %s' % inv_brw.name),
                                  'type': type_invoice,
                                  'account_id': acc_id,
                                  'partner_id': acc_part_id.id,
                                  'journal_id': journal,
                                  'date_ret': inv_brw.date,
                                  'period_id': inv_brw.date,
                                  'date': inv_brw.date,
                                  }
                    else:
                        if inv_brw.move_type in ('in_invoice', 'in_refund'):
                            if inv_brw.move_type == 'in_invoice' and inv_brw.debit_origin_id:
                                type_invoice = 'in_debit'
                            elif not inv_brw.debit_origin_id and inv_brw.move_type in ('in_refund', 'in_invoice'):
                                type_invoice = inv_brw.move_type

                        if not acc_id:
                            raise UserError(
                                _('Invalid Action !' 'You need to configure the partner with'
                                  ' withholding accounts!'))
                        values = {'name': _('IVA WH - ORIGIN %s' % inv_brw.supplier_invoice_number),
                                  'type': type_invoice,
                                  'account_id': acc_id,
                                  'partner_id': acc_part_id.id,
                                  'date_ret': inv_brw.date,
                                  'period_id': inv_brw.date,
                                  'date': inv_brw.date,
                                  }
                ret_id = wh_iva_obj.create(values)

                ret_id.write({'wh_lines': [(4, ret_line_id.id)]})
                if hasattr(ret_id, 'id'): ret_id = ret_id.id
                if ret_id:
                    inv.write({'wh_iva_id': ret_id})
                    inv.wh_iva_id.compute_amount_wh()
        return True

    def button_reset_taxes_ret(self):
        """ Recalculate taxes in invoice
        """
        account_invoice_tax = self.env['account.tax']
        for inv in self:
            compute_taxes_ret = account_invoice_tax.compute_amount_ret(inv)
            for tax in account_invoice_tax.browse(compute_taxes_ret.keys()):
                tax.write(compute_taxes_ret[tax.id])
        return True

    def button_reset_taxes(self):
        """ It makes two function calls related taxes reset
        """
        res = super(AccountMove, self).button_reset_taxes()
        self.button_reset_taxes_ret()
        return res

    def _withholding_partner(self):
        """ I verify that the provider retains or not
        """
        # No VAT withholding Documents are created for customer invoice &
        # refunds
        for inv in self:
            if inv.move_type in ('in_invoice', 'in_refund', 'out_invoice', 'out_refund') and \
                    inv.company_id.partner_id.wh_iva_agent:
                return True
        return False

    def _withholdable_tax(self):
        """ Verify that existing withholding in invoice
        """
        is_withholdable = False
        for inv in self.line_ids:
            for tax in inv.tax_ids:
                if tax.type_tax == 'iva' and tax.amount > 0:
                    is_withholdable = True
        return is_withholdable

    def check_withholdable(self):
        """ This will test for Refund invoice trying to find out
        if its regarding parent is in the same fortnight.

        return True if invoice is type 'in_invoice'
        return True if invoice is type 'in_refund' and parent_id invoice
                are both in the same fortnight.
        return False otherwise
        """
        # period = self.env['account.period']
        for inv in self:
            if inv.move_type == 'in_invoice':
                return True
            if inv.move_type == 'out_invoice':
                return True
            '''
            if inv.move_type == 'in_refund' and inv.parent_id:
                dt_refund = inv.invoice_date or time.strftime('%Y-%m-%d')
                dt_invoice = inv.parent_id.invoice_date
                return period.find_fortnight(dt_refund) == period.find_fortnight(dt_invoice)
            '''
        return False

    def check_wh_apply(self):
        """ Apply withholding to the invoice
        """
        wh_apply = []
        for inv in self:
            if inv.vat_apply or inv.sin_cred:
                return False
            wh_apply.append(inv._withholdable_tax())
            wh_apply.append(inv._withholding_partner())
        return all(wh_apply)

    def validate_wh_iva_done(self):
        """ Method that check if wh vat is validated in invoice refund.
        return: True: the wh vat is validated.
                False: the wh vat is not validated.
        """
        for inv in self:
            if inv.move_type in ('out_invoice', 'out_refund') and not inv.wh_iva_id:
                riva = True
            else:
                riva = (not inv.wh_iva_id and True or
                        inv.wh_iva_id.state in 'posted' and True or False)
                if not riva:
                    raise UserError(
                        _('Error !' '¡La retención de IVA "% s" no está validada!' %
                          inv.wh_iva_id.code))
        return True

    def action_cancel(self):
        """ Verify first if the invoice have a non cancel withholding iva doc.
        If it has then raise a error message. """
        for inv in self:
            if ((not inv.wh_iva_id) or (
                    inv.wh_iva_id and
                    inv.wh_iva_id.state == 'cancel')):
                super(AccountMove, self).action_cancel()
            else:
                raise UserError(
                    _("Error!" "No puede cancelar una factura que no se encuentra cancelado"
                      "el documento de retención. Primero debe cancelar la factura"
                      "documento de retención y luego puede cancelar esto"
                      "factura"))
        return True

    def _get_move_lines1(self, to_wh, journal_id, writeoff_account_id, writeoff_journal_id,
                         date, name):
        """ Generate move lines in corresponding account
        @param to_wh: whether or not withheld
        @param writeoff_journal_id: journal where canceled
        @param date: current date
        @param name: description
        """
        res = []
        acc = None
        for invoice in self:
            acc_part_id = self.env['res.partner']._find_accounting_partner(invoice.partner_id)
            types = {'out_invoice': -1,
                     'out_refund': 1}
            direction = types[invoice.move_type]
            print("to_wh: ", to_wh)
            amount_ret2 = 0
            for tax_brw in to_wh:
                if 'invoice' in invoice.move_type:
                    acc = (tax_brw.wh_vat_line_id.retention_id.journal_id.default_iva_account.id and
                           tax_brw.wh_vat_line_id.retention_id.journal_id.default_iva_account.id or
                           False)
                elif 'refund' in invoice.move_type:
                    acc = (tax_brw.wh_vat_line_id.retention_id.journal_id.default_iva_account.id and
                           tax_brw.wh_vat_line_id.retention_id.journal_id.default_iva_account.id or
                           False)
                if not acc:
                    raise UserError(
                        _('¡Falta una cuenta en impuestos!\n')
                        ("El impuesto [% s] tiene una cuenta faltante. Por favor, complete el "
                         "campos faltantes") % (tax_brw.name))
                amount_ret2 += tax_brw.amount_ret
            res.append((0, 0, {
                'debit':
                    direction * amount_ret2 < 0 and direction * amount_ret2,
                'credit':
                    direction * amount_ret2 > 0 and direction * amount_ret2,
                'account_id': acc,
                'partner_id': acc_part_id.id,
                'ref': invoice.name,
                'date': date,
                'name': name,
                'amount_residual': direction * amount_ret2,
                'currency_id': False,
            }))
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('tax_ids')
    def add_retention_tax(self):
        if self.move_id.move_type in ('in_invoice', 'in_refund', 'in_debit'):
            for tax in self.tax_ids:
                if tax.type_tax == 'iva' and tax.amount > 0:
                    if self.move_id.partner_id.tax_percentage:
                        id = self.move_id.partner_id.tax_percentage.id
                        self.tax_ids = [(4, id)]
                        self.move_id._compute_invoice_taxes_by_group()