# -*- coding: utf-8 -*-

from odoo import models, _, fields, api


class AccountMoveReversalInherit(models.TransientModel):
    _inherit = 'account.move.reversal'

    nro_ctrl = fields.Char(
        'Número de Control', size=32,
        help="Número utilizado para gestionar facturas preimpresas, por ley "
             "Necesito poner aquí este número para poder declarar"
             "Informes fiscales correctamente.", store=True)
    supplier_invoice_number = fields.Char(
        string='Número de factura del proveedor', size=64,
        store=True)
    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven

    def _get_sequence_code(self):
        # metodo que crea la secuencia del número de control, si no esta creada crea una con el
        # nombre: 'l10n_nro_control
        self.ensure_one()
        sequence_code = 'l10n_nro_control_sale'
        company_id = self.env.company
        ir_sequence = self.env['ir.sequence'].with_context(force_company=company_id.id)
        nro_ctrl = ir_sequence.next_by_code(sequence_code)
        return nro_ctrl
    def reverse_moves(self):
        moves = self.env['account.move'].browse(self.env.context['active_ids']) if self.env.context.get('active_model') == 'account.move' else self.move_id

        # Create default values.
        default_values_list = []
        for move in moves:
            default_values_list.append(self._prepare_default_reversal(move))


        batches = [
            [self.env['account.move'], [], True],   # Moves to be cancelled by the reverses.
            [self.env['account.move'], [], False],  # Others.
        ]
        for move, default_vals in zip(moves, default_values_list):
            is_auto_post = bool(default_vals.get('auto_post'))
            is_cancel_needed = not is_auto_post and self.refund_method in ('cancel', 'modify')
            batch_index = 0 if is_cancel_needed else 1
            batches[batch_index][0] |= move
            batches[batch_index][1].append(default_vals)

        # Handle reverse method.
        moves_to_redirect = self.env['account.move']
        for moves, default_values_list, is_cancel_needed in batches:
            if default_values_list:
                default_values_list[0]['supplier_invoice_number'] = self.supplier_invoice_number
                default_values_list[0]['nro_ctrl'] = self.nro_ctrl
                if not default_values_list[0]['nro_ctrl']:
                    default_values_list[0]['nro_ctrl'] = self._get_sequence_code()
            new_moves = moves._reverse_moves(default_values_list, cancel=is_cancel_needed)
            if new_moves.state != 'draft':
                new_moves.attach_iva_to_credit_note()
            if new_moves.reversed_entry_id:
                new_moves.invoice_reverse_purchase_id = new_moves.reversed_entry_id
            # if new_moves:
            #     new_moves.supplier_invoice_number_aux.name = new_moves.supplier_invoice_number

            if self.refund_method == 'modify':
                moves_vals_list = []
                for move in moves.with_context(include_business_fields=True):
                    moves_vals_list.append(move.copy_data({'date': self.date or move.date})[0])
                new_moves = self.env['account.move'].create(moves_vals_list)

            moves_to_redirect |= new_moves

        # Create action.
        action = {
            'name': _('Reverse Moves'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
        }
        if len(moves_to_redirect) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': moves_to_redirect.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', moves_to_redirect.ids)],
            })
        return action
