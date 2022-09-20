# coding: utf-8

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, date
from dateutil import relativedelta

_DATETIME_FORMAT = "%Y-%m-%d"


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _get_default_invoice_date(self):
        return fields.Date.today() if self._context.get('default_move_type', 'entry') in \
                                      ('in_invoice', 'in_refund', 'in_receipt') else False

    @api.model_create_multi
    def create(self, values):
        res = super(AccountMove, self).create(values)
        for line in res:
            if line.invoice_date and line.date:
                if line.invoice_date > line.date:
                    raise Warning(_('La fecha contable no puede ser menor a la fecha de la factura'))
        return res


    def write(self, vals):
        for record in self:
            if vals.get('move_type') in ('out_invoice', 'out_refund') and \
                    vals.get('date') and not vals.get('date_document'):
                vals['date_document'] = vals['date']
            if vals.get('supplier_invoice_number', False):
                supplier_invoice_number_id = record._unique_invoice_per_partner('supplier_invoice_number',
                                                                              vals.get('supplier_invoice_number', False))
                if not supplier_invoice_number_id:
                    record.supplier_invoice_number = False
                    return {'warning': {'title': "Advertencia!",
                                        'message': "  El Numero de la Factura del Proveedor ya Existe  "}}
            if vals.get('nro_ctrl', False):
                if not record.maq_fiscal_p and not vals.get('maq_fiscal_p', False):
                    nro_ctrl_id = record._unique_invoice_per_partner('nro_ctrl', vals.get('nro_ctrl', False))
                    if not nro_ctrl_id:
                        self.nro_ctrl = False
                        return {'warning': {'title': "Advertencia!",
                                            'message': "  El Numero de control de la Factura del Proveedor ya Existe  "}}
            if not vals.get('check_fiscal'):
                if vals.get('invoice_date') and isinstance(vals.get('invoice_date'), str):
                    fecha_factura = datetime.strptime(vals.get('invoice_date'), '%Y-%m-%d').date()
                else:
                    if vals.get('invoice_date'):
                        fecha_factura = vals.get('invoice_date')
                    elif len(self) < 2:
                        fecha_factura = record.invoice_date
                    else:
                        fecha_factura = False
                if vals.get('date') and isinstance(vals.get('invoice_date'), str):
                    fecha = datetime.strptime(vals.get('date'), '%Y-%m-%d').date()
                else:
                    if vals.get('date'):
                        fecha = vals.get('date')
                    elif len(self) < 2:
                        fecha = record.date
                    else:
                        fecha = False
                #Doing a good formating of dates
                if type(fecha) == str:
                    fecha = datetime.strptime(fecha, '%Y-%m-%d')
                    if type(fecha_factura) == str:
                        fecha_factura = datetime.strptime(fecha_factura, '%Y-%m-%d')
                    else:
                        fecha_factura = fecha_factura.strftime('%Y-%m-%d')
                        fecha_factura = datetime.strptime(fecha_factura, '%Y-%m-%d')
                if type(fecha_factura) == str:
                    fecha_factura = datetime.strptime(fecha_factura, '%Y-%m-%d')
                    if type(fecha) == str:
                        fecha = datetime.strptime(fecha, '%Y-%m-%d')
                    else:
                        fecha = fecha.strftime('%Y-%m-%d')
                        fecha = datetime.strptime(fecha, '%Y-%m-%d')

                if fecha and fecha_factura:
                    if fecha_factura > fecha:
                        raise Warning(_('La fecha contable no puede ser menor a la fecha de la factura'))
            else:
                del vals['check_fiscal']
        return super(AccountMove, self).write(vals)

    supplier_invoice_number = fields.Char(string='Supplier Invoice Number', store=True,
                                          help="The reference of this invoice as provided by the supplier.")
    nro_ctrl = fields.Char(string='Control Number', size=32,
                           help="Number used to manage pre-printed invoices, by law you will need to put here this "
                                "number to be able to declarate on Fiscal reports correctly.", store=True)
    loc_req = fields.Boolean(string='Maquina Fiscal?', default=lambda s: s._get_loc_req(),
                             help='This fields is for technical use')
    sin_cred = fields.Boolean(string='Excluir este documento del libro fiscal', readonly=False,
        help="Configúrelo verdadero si la factura está exenta de IVA (exención de impuestos)")

    date_document = fields.Date(string='Document Date', states={'draft': [('readonly', False)]},
                                help="Fecha administrativa, generalmente es la fecha impresa en factura, esta fecha se"
                                     " utiliza para mostrar en la compra fiscal libro")
    invoice_printer = fields.Char(string='Número de factura de impresora fiscal', size=64, required=False,
                                  help="Fiscal printer invoice number, is the number of the invoice"
                                       " on the fiscal printer")
    invoice_reverse_purchase_id = fields.Many2one('account.move', string="Reversal invoice purchase", copy=False)
    fiscal_printer = fields.Char(string='Número Impresora Fiscal', size=64, required=False,
                                 help="Fiscal printer number, generally is the id number of the printer.")
    z_report = fields.Char(string='Report Z', size=64)
    comment_paper = fields.Char(string='Comentario')
    paper_anu = fields.Boolean(string='Papel Dañado', default=False)
    marck_paper = fields.Boolean(default=False)
    maq_fiscal_p = fields.Boolean(string='Maquina Fiscal', default=False)

    def _get_journal(self, context):
        """ Return the journal which is
        used in the current user's company, otherwise
        it does not exist, return false
        """
        context = context or {}
        res = super(AccountMove, self)._get_journal(context)
        if res:
            return res
        type_inv = context.get('type', 'sale')
        if type_inv in ('sale_debit', 'purchase_debit'):
            user = self.env['res.users'].browse(context)
            company_id = context.get('company_id', user.company_id.id)
            journal_obj = self.env['account.journal']
            domain = [('company_id', '=', company_id), ('type', '=', type_inv)]
            res = journal_obj.search(domain, limit=1)
        return res and res[0] or False

    def _unique_invoice_per_partner(self, field, value):
        """ Return false when it is found
        that the bill is not out_invoice or out_refund,
        and it is not unique to the partner.
        """
        ids_ivo = []
        for inv in self:
            ids_ivo.append(inv.id)
            if inv.move_type in ('out_invoice', 'out_refund'):
                return True
            inv_ids = (
                self.search([(field, '=', value), ('move_type', '=', inv.move_type), ('partner_id', '=', inv.partner_id.id)]))

            if [True for i in inv_ids if i not in ids_ivo] and inv_ids:
                return False
        return True

    def _get_loc_req(self):
        """Get if a field is required or not by a Localization
        @param uid: Integer value of the user
        """
        context = self._context or {}
        res = True
        ru_brw = self.env['res.users'].browse(self._uid)
        rc_obj = self.env['res.company']
        rc_brw = rc_obj.browse(ru_brw.company_id.id)
        if rc_brw.country_id and rc_brw.country_id.code == 'VE' and \
                rc_brw.printer_fiscal:
            res = False
        return res

    # Validaciónn de Fecha
    @api.onchange('date_document')
    def onchange_date_document(self):
        fecha = self.date_document
        if fecha:
            fecha2 = str(fecha)
            age = self._calculate_date(fecha2)
            if age:
                if age.days >= 0 and age.months >= 0 and age.years >= 0:
                    self.date_document = fecha
                else:
                    self.date_document = False
                    return {'warning': {'title': "Advertencia!",
                                        'message': "La fecha ingresada es mayor que la fecha actual"}}

    @staticmethod
    def _calculate_date(value):
        age = 0
        if value:
            ahora = datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)

            age = relativedelta.relativedelta(datetime.strptime(ahora, _DATETIME_FORMAT),
                                              datetime.strptime(value, _DATETIME_FORMAT))
        return age

    def copy(self, default=None):
        res = super(AccountMove, self).copy(default)
        return res

    @api.onchange('supplier_invoice_number')
    def onchange_supplier_invoice_number(self):
        if self.supplier_invoice_number:
            supplier_invoice_number_id = self._unique_invoice_per_partner('supplier_invoice_number', self.supplier_invoice_number)
            if not supplier_invoice_number_id:
                self.supplier_invoice_number = False
                return {'warning': {'title': "Advertencia!",
                                    'message': "  El Numero de la Factura del Proveedor ya Existe  "}}

    @api.onchange('nro_ctrl')
    def onchange_nro_ctrl(self):
        if self.nro_ctrl:
            if not self.maq_fiscal_p:
                nro_ctrl_id = self._unique_invoice_per_partner('nro_ctrl', self.nro_ctrl)
                if not nro_ctrl_id:
                    self.nro_ctrl = False
                    return {'warning': {'title': "Advertencia!",
                                        'message': "  El Numero de control de la Factura del Proveedor ya Existe  "}}


class AccountInvoiceTax(models.Model):
    _inherit = 'account.tax'

    tax_id = fields.Many2one('account.tax', string='Tax', required=False, ondelete='set null',
                             help="Tax relation to original tax, to be able to take off all data from invoices.")
