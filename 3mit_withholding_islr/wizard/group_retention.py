from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError

class GroupRetentionISLR(models.TransientModel):
    _name = 'wizard.group.retention.islr'

    start_date = fields.Date('Desde')
    final_date = fields.Date('Hasta')
    retentions = fields.Many2many('islr.wh.doc', string='Retenciones asociadas')

    def generate_retention_islr(self):
        self.validar_fecha()
        rets = self.create_retentions()
        return {
            'name': 'Retenciones',
            'view_mode': 'tree,form',
            'res_model': 'wh.islr.group',
            'domain': "[('id', 'in', %s)]" % rets,
            'type': 'ir.actions.act_window'
        }

    def validar_fecha(self):
        if self.start_date and self.final_date:
            if self.start_date > self.final_date:
                raise exceptions.ValidationError('Introduzca una fecha final igual o mayor a la incial')
        else:
            raise exceptions.ValidationError('Introduzca una fecha Inicial y una final')

    def create_retentions(self):
        rets = []
        invoice_ids = self.env['account.move'].search([('move_type', 'in', ['in_refund', 'in_invoice']), ('date', '>=', self.start_date), ('date', '<=', self.final_date), ('islr_wh_doc_id', '=', False), ('company_id', '=', self.env.company.id), ('state', '=', 'posted')], order="date ASC")
        for invoice in invoice_ids:
            esRetencionISLR = False
            concepts = invoice.get_islr_concepts()
            if len(concepts) > 0 and invoice.partner_id.islr_withholding_agent:
                esRetencionISLR = True

            if not esRetencionISLR:
                invoice_ids -= invoice

        if len(invoice_ids) > 0:
            partners = list(map(lambda invoice: invoice.partner_id, invoice_ids))
            partners = list(set(partners))
            for partner in partners:
                invoices = invoice_ids.filtered(lambda line: line.partner_id.id == partner.id)
                ids = []
                for invoice in invoices:
                    ids.append(invoice.id)
                vals = {
                    'fecha_contable': self.final_date,
                    'invoice_ids': ids,
                    'fecha_del_vale': self.final_date,
                    'partner_id': partner.id,
                }
                retention = self.env['wh.islr.group'].create(vals)
                retention.update_lines()
                rets.append(retention.id)
        else:
            raise UserError("No hay ninguna factura de proveedor con impuesto de retención ISLR en este rango de fechas.")
        return rets