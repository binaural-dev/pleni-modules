# coding: utf-8
###########################################################################

import base64
import odoo.addons as addons
from odoo import models, fields, api
from odoo.exceptions import UserError


class WhIslrGroup(models.Model):
    _name = 'wh.islr.group'

    invoice_ids = fields.Many2many('account.move', string='Facturas Incluidas para retención', domain=[("move_type", "in", ["in_invoice", "in_refund"])])
    retentions = fields.Many2many('islr.wh.doc', string='Retenciones asociadas')
    partner_id = fields.Many2one('res.partner', string='Proveedor')
    fecha_contable = fields.Date()
    fecha_del_vale = fields.Date()
    number_ret = fields.Char()
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('cancel', 'Cancelado')], string='Estado', readonly=True, default='draft',
        help="Estado de retención")
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

    def unlink(self):
        for element in self:
            for retention in element.retentions:
                retention.action_cancel()
                retention.unlink()
        return super(WhIslrGroup, self).unlink()

    def action_confirm(self):
        if not self.retentions:
            raise UserError("Primero genere las líneas de retenciones")
        if not self.number_ret:
            self.number_ret = self._get_sequence_code()
        for i in self.retentions:
            i.number = self.number_ret
            i.action_confirm()
        self.write({'state': 'confirmed'})
        return True

    def set_to_draft(self):
        self.write({'state': 'draft'})
        return True

    def update_lines(self):
        add_rets = []
        for i in self.invoice_ids:
            if not i.islr_wh_doc_id:
                i.make_retention()
            if i.islr_wh_doc_id:
                add_rets.append(i.islr_wh_doc_id.id)
        if add_rets:
            self.write({'retentions': add_rets})

    def _get_sequence_code(self):
        # metodo que crea la secuencia del número de control, si no esta creada crea una con el
        # nombre: 'l10n_nro_control
        SEQUENCE_CODE = 'islr.wh.doc'
        IrSequence = self.env['ir.sequence'].with_context(force_company=self.company_id.id)
        self.number_ret = IrSequence.next_by_code(SEQUENCE_CODE)
        return self.number_ret