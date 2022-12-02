from odoo import models, fields, exceptions, _
from odoo.exceptions import Warning


class GroupRetention(models.TransientModel):
    _name = 'wizard.group.retention'

    start_date = fields.Date('Desde')
    final_date = fields.Date('Hasta')

    def generate_retention_iva(self):
        self.validar_fecha()
        rets = self.create_retentions()
        return {
            'name': 'Retenciones',
            'view_mode': 'tree,form',
            'res_model': 'wh.iva.group',
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
        invoice_ids = self.env['account.move'].search(
            [('move_type', 'in', ('in_refund', 'in_invoice')), ('wh_iva_id', '!=', False),
             ('wh_iva_id.state', '=', 'draft'), '&', ('date', '>=', self.start_date),
             ('date', '<=', self.final_date)])
        partners = list(map(lambda invoice: invoice.partner_id, invoice_ids))
        partners = list(set(partners))
        partners = list(filter(lambda partner: partner.wh_iva_agent, partners))
        for partner in partners:
            invoices = invoice_ids.filtered(lambda line: line.partner_id.id == partner.id)
            vals = {
                'fecha_contable': self.final_date,
                'invoice_ids': invoices,
                'fecha_del_vale': self.final_date,
                'partner_id': partner.id,
            }
            retention = self.env['wh.iva.group'].create(vals)
            retention.update_lines()
            rets.append(retention.id)
        return rets
