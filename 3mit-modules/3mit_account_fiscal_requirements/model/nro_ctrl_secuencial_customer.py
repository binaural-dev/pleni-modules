# coding: utf-8

from odoo import models, fields, api
from odoo.tools.translate import _
from datetime import datetime,date
from dateutil import relativedelta


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    nro_ctrl = fields.Char(string='Número de Control', size=32,
                           help="Número utilizado para gestionar facturas preimpresas, por ley Necesito poner aquí este"
                                " número para poder declarar Informes fiscales correctamente.", copy=False, store=True)

    def _get_company(self):
        res_company = self.env['res.company'].search([('id', '=', self.company_id.id)])
        return res_company

    def action_post(self):
        var = super(AccountMoveInherit, self).action_post()
        for i in self:
            if i.move_type in ['out_invoice', 'out_refund']:
                if not i.nro_ctrl:
                    i.nro_ctrl = i._get_sequence_code()
                    i.write({'nro_ctrl': i.nro_ctrl})
        # if self.move_type in 'out_refund':
        #     if not self.nro_ctrl:
        #         name_factc = self.reversed_entry_id.display_name
        #         factc_affect = self.env['account.move'].search([('name', '=', name_factc)])
        #         nro_ctrl = factc_affect.nro_ctrl
        #         self.write({'nro_ctrl': nro_ctrl})
        return var

    def _get_sequence_code(self):
        # metodo que crea la secuencia del número de control, si no esta creada crea una con el
        # nombre: 'l10n_nro_control
        self.ensure_one()
        sequence_code = 'l10n_nro_control_sale'
        company_id = self._get_company()
        ir_sequence = self.env['ir.sequence'].with_context(force_company=company_id.id)
        self.nro_ctrl = ir_sequence.next_by_code(sequence_code)
        return self.nro_ctrl
