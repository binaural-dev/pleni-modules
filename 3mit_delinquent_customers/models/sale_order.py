# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo.exceptions import AccessDenied
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_due = fields.Monetary(related='partner_id.amount_due')

    # TODO: Revisar funcionamiento de la funcion
    def action_confirm(self):
        '''
        Check the partner credit limit and exisiting due of the partner
        before confirming the order. The order is only blocked if exisitng
        due is greater than blocking limit of the partner.
        '''
        partner_id = self.partner_id
        total_amount = self.amount_due
        if partner_id.delinquent_check:
            if partner_id.invalid_invoices_qty:
                raise AccessDenied(_(
                    f"""El cliente tiene facturas vencidas. Cancele las facturas anteriores antes de generar nuevos pedidos.

Facturas Vencidas: {partner_id.invalid_invoices_qty}
Dueda Total: {partner_id.foreign_currency.symbol} {partner_id.amount_due}"""))

            # existing_move = self.env['account.move'].search(
                # [('partner_id', '=', self.partner_id.id), ('state', '=', 'posted'), ('invoice_date_due','<',date.today())])
            # if partner_id.invalid_invoices_limit <= partner_id.invalid_invoices_qty:
            #     raise AccessDenied(_('Customer has 2 o more unpayed invoices.'))
            # elif partner_id.credit_blocking <= total_amount and not existing_move:
            #     view_id = self.env.ref('ob_customer_credit_limit.view_warning_wizard_form')
            #     context = dict(self.env.context or {})
            #     context['message'] = "Customer Blocking limit exceeded without having a recievable, Do You want to continue?"
            #     context['default_sale_id'] = self.id
            #     if not self._context.get('warning'):
            #         return {
            #             'name': 'Warning',
            #             'type': 'ir.actions.act_window',
            #             'view_mode': 'form',
            #             'res_model': 'warning.wizard',
            #             'view_id': view_id.id,
            #             'target': 'new',
            #             'context': context,
            #         }
            # elif partner_id.credit_warning <= total_amount and partner_id.credit_blocking > total_amount:
            #     view_id = self.env.ref('ob_customer_credit_limit.view_warning_wizard_form')
            #     context = dict(self.env.context or {})
            #     context['message'] = "Customer warning limit exceeded, Do You want to continue?"
            #     context['default_sale_id'] = self.id
            #     if not self._context.get('warning'):
            #         return {
            #             'name': 'Warning',
            #             'type': 'ir.actions.act_window',
            #             'view_mode': 'form',
            #             'res_model': 'warning.wizard',
            #             'view_id': view_id.id,
            #             'target': 'new',
            #             'context': context,
            #         }
            # elif partner_id.credit_blocking <= total_amount:
            #     raise AccessDenied(_('Customer credit limit exceeded.'))
        res = super(SaleOrder, self).action_confirm()
        return res
