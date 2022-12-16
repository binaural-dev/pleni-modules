# coding: utf-8
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    Copyright (C) OpenERP Venezuela (<http://openerp.com.ve>).
#    All Rights Reserved
###############################################################################
#    Credits:
#    Coded by: Maria Gabriela Quilarque  <gabriela@openerp.com.ve>
#    Planified by: Nhomar Hernandez
#    Finance by: Helados Gilda, C.A. http://heladosgilda.com.ve
#    Audited by: Humberto Arocha humberto@openerp.com.ve
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

#from openerp.report import report_sxw
#from openerp.tools.translate import _

from odoo import models, api, _
from odoo.exceptions import UserError, Warning
from odoo import api, fields, models, _
from odoo import exceptions


class RepComprobanteIslr(models.AbstractModel):
    _name = 'report.3mit_withholding_islr.template_wh_islr'
    _description = 'Report 3mit withholding ISLR template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not docids:
            raise UserError("Necesita seleccionar una retencion para imprimir.")
        data = {'form': self.env['islr.wh.doc'].browse(docids)}
        res = dict()
        partner_id = data['form'].partner_id
        total_doc = data['form'].invoice_id.amount_total_conversion if data['form'].invoice_id.currency_id.name == "USD" else data['form'].invoice_id.amount_total
        date_ret = data['form'].date_ret
        if data["form"].type in ["out_invoice", "out_refund"]:
            raise UserError("Error! El comprobante de retención no está disponible en facturas de cliente.")
        if date_ret:
            split_date = (str(date_ret).split('-'))
            date_ret = str(split_date[2]) + '/' + (split_date[1]) + '/' + str(split_date[0])
            period_date = (str(data['form'].date_ret).split('-'))
            period = str(period_date[1]) + '/' + str(period_date[0])
        else:
            raise Warning(_("Se necesita la Fecha para poder procesar."))
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

        if data['form'].state == 'confirmed':
            return {
                'data': data['form'],
                'document': document,
                'total_doc': total_doc,
                'model': self.env['report.3mit_withholding_islr.template_wh_islr'],
                'doc_model': self.env['report.3mit_withholding_islr.template_wh_islr'],
                'lines': res,
                'date_ret': date_ret,
                'period': period,
            }
        else:
            raise UserError("La Retencion de ISLR debe estar en estado Confirmado para poder generar su Comprobante")

    def obtener_tasa(self, invoice):
        fecha = invoice.invoice_date
        tasa_id = invoice.currency_id
        tasa = self.env['res.currency.rate'].search([('currency_id', '=', tasa_id.id), ('name', '<=', fecha)],
                                                 order='id desc', limit=1)
        if not tasa:
            raise UserError("Advertencia! \nNo hay referencia de tasas registradas para moneda USD en la fecha igual o inferior de la factura %s" % (invoice.name))

        return tasa.rate
                
    def _get_date_invoice(self, id):

        date_invoice = id[0].invoice_id.date_document
        return date_invoice

    def _get_supplier_invoice_number(self, id):

        supplier_number = id[0].invoice_id.supplier_invoice_number
        return supplier_number

    def _get_nro_ctrl(self, id):

        nro_ctrl = id[0].invoice_id.nro_ctrl
        return nro_ctrl

    def _get_islr_wh_concept(self,id):

        concept = id[0].concept_id.name

        return concept

    def _get_islr_wh_retencion_islr(self,id):

        retencion_islr_local = id[0].retencion_islr
        return retencion_islr_local

    def _get_islr_wh_doc_invoices_base(self,id):
        base_ret_local = id[0].base_amount
        return base_ret_local

    def _get_islr_wh_doc_invoice_subtract(self,id):

        subtract_local = id[0].subtract
        return subtract_local

    def _get_islr_invoice_amount_ret(self,id):

        amount_ret_local = id[0].amount
        return amount_ret_local

    def _get_islr_invoice_amount_ret_tax_ut(self,id):

        amount_ret_local_tax_ut = id[0].raw_tax_ut
        return amount_ret_local_tax_ut


    def get_period(self, date):
        if not date:
            raise Warning(_("Se necesita una fecha, por favor ingresar"))
        split_date = str(date).split('-')
        return str(split_date[1]) + '/' + str(split_date[0])

    def get_date(self, date):
        if not date:
            raise Warning(_("Se necesita una fecha, por favor ingresar."))
        split_date = date.split('-')
        return str(split_date[2]) + '/' + (split_date[1]) + '/' + str(split_date[0])


    def get_direction(self, partner):
        direction = ''
        direction = ((partner.street and partner.street + ', ') or '') + \
                    ((partner.street2 and partner.street2 + ', ') or '') + \
                    ((partner.city and partner.city + ', ') or '') + \
                    ((partner.state_id.name and partner.state_id.name + ',')or '')+ \
                    ((partner.country_id.name and partner.country_id.name + '') or '')
        if direction == '':
            direction = 'Sin direccion'
        return direction

    def get_tipo_doc(self, tipo=None):
        if not tipo:
            return []
        types = {'out_invoice': '1', 'in_invoice': '1', 'out_refund': '2',
                 'in_refund': '2'}
        return types[tipo]
