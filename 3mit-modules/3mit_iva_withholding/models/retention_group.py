# -*- coding: utf-8 -*-

import base64
import odoo.addons as addons
from odoo import models, fields, exceptions, api
from odoo.exceptions import UserError


class WhIvaGroup(models.Model):
    _name = 'wh.iva.group'
    _description = 'Withholding iva group'

    invoice_ids = fields.Many2many('account.move', string='Facturas Incluidas para retención', name_get='new_names')
    retentions = fields.Many2many('account.wh.iva', string='Retenciones asociadas')
    partner_id = fields.Many2one('res.partner', string='Proveedor')
    fecha_contable = fields.Date()
    fecha_del_vale = fields.Date()
    number_ret = fields.Char()
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Realizado'),
        ('cancel', 'Cancelado')], string='Estado', readonly=True, default='draft',
        help="Estado de retención")
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

    def action_confirm(self):
        if not self.retentions:
            raise UserError("Primero genere las líneas de retenciones")
        if not self.number_ret:
            self.number_ret = self._get_sequence_code()
        for i in self.retentions:
            i.number = self.number_ret
            i.number_2 = self.number_ret
            i.confirm_check()
            self.write({'state': 'done'})

    def set_to_draft(self):
        self.write({'state': 'draft'})
        return True

    def update_lines(self):
        add_rets = []
        for i in self.invoice_ids:
            if i.wh_iva_id:
                add_rets.append(i.wh_iva_id.id)
        if add_rets:
            self.write({'retentions': add_rets})
        for i in self.retentions:
            for j in i.wh_lines.tax_line:
                j._get_only_amount()
                j._get_amount_ret()

    def _get_sequence_code(self):
        # metodo que crea la secuencia del número de control, si no esta creada crea una con el
        # nombre: 'l10n_nro_control
        SEQUENCE_CODE = 'number_comprobante'
        IrSequence = self.env['ir.sequence']
        local_number = IrSequence.next_by_code(SEQUENCE_CODE)
        if local_number and self.fecha_contable:
            account_month = str(self.fecha_contable).split('-')[1]
            account_year = str(self.fecha_contable).split('-')[0]
            if not account_month == local_number[4:6] or not account_year == local_number[:4]:
                local_number = account_year + account_month + local_number[6:]
        self.number_ret = local_number
        return self.number_ret

    def name_get(self, ):
        res = []
        for item in self:
            if item.number_ret and item.state == 'done':
                res.append((item.id, '%s (%s)' % (item.number_ret, 'WH IVA')))
            else:
                res.append((item.id, '%s' % ('WH IVA Draft')))
        return res
