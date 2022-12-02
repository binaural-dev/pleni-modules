from odoo.exceptions import UserError
from odoo import api, fields, models, _


class RepComprobanteIslrGroup(models.AbstractModel):
    _name = 'report.3mit_withholding_islr.template_wh_islr_group'

    def split_fecha(self,fecha):
        split_date = (str(fecha).split('-'))
        fecha_f = str(split_date[2]) + '/' + (split_date[1]) + '/' + str(split_date[0])
        return fecha_f

    @api.model
    def _get_report_values(self, docids, data=None):
        if len(docids) != 1:
            raise UserError("Seleccione una sola retencion para imprimir")
        form = self.env['wh.islr.group'].browse(docids)
        if form.state != 'confirmed':
            raise UserError("La Retencion de ISLR debe estar en estado Confirmado para poder generar su Comprobante")
        else:
            company = form.company_id
            partner_id = form.partner_id
            date_ret = self.split_fecha(form.fecha_contable)
            period_date = (str(form.fecha_del_vale).split('-'))
            period = str(period_date[1]) + '/' + str(period_date[0])
            if company.partner_id.contact_address_complete:
                direccion = company.partner_id.contact_address_complete
            else:
                direccion = ''
            if partner_id.company_type == 'person':
                if partner_id.rif:
                    document = partner_id.rif
                else:
                    if partner_id.nationality == 'V' or partner_id.nationality == 'E':
                        document = str(partner_id.nationality) + str(partner_id.identification_id)
                    else:
                        document = str(partner_id.identification_id)
            else:
                document = partner_id.rif
            if partner_id.contact_address_complete:
                direccion_ret = partner_id.contact_address_complete
            else:
                direccion_ret = ''
            if partner_id.phone:
                telefono = partner_id.phone
            else:
                telefono = ''
            line = 0
            total_ret = 0
            res = []
            for ret in form.retentions:
                for invoice in ret.concept_ids:
                    rec = {'fecha': self.split_fecha(invoice.invoice_id.invoice_date),
                           'numero_fact': invoice.invoice_id.supplier_invoice_number,
                           'n_control': invoice.invoice_id.nro_ctrl,
                           'concepto_ret': invoice.concept_id.display_name,
                           'total_doc': invoice.invoice_id.amount_total_conversion if invoice.invoice_id.currency_id.name == "USD" else invoice.invoice_id.amount_total,
                           'base_amount': invoice.base_amount,
                           'retencion_islr': invoice.retencion_islr,
                           'amount': invoice.amount,
                           'subtract': invoice.subtract,
                           'raw_tax_ut': invoice.raw_tax_ut,
                           }
                    res.insert(line, rec)
                    line += 1
                total_ret += ret.amount_total_ret
            return {
                'document': document,
                'company': company,
                'partner_id': partner_id,
                'res': res,
                'date_ret': date_ret,
                'period': period,
                'direccion': direccion,
                'direccion_ret': direccion_ret,
                'telefono': telefono,
                'total_ret': total_ret,
            }
