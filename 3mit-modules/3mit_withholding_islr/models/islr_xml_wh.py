# coding: utf-8
import datetime
import logging
import base64
import time
from xml.etree.ElementTree import Element, SubElement, tostring
from odoo.exceptions import UserError

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)
ISLR_XML_WH_LINE_TYPES = [('invoice', 'Invoice'), ('employee', 'Employee')]


class IslrXmlWhDoc(models.Model):
    _name = "islr.xml.wh.doc"
    _description = 'Generate XML'

    def delete_employee_xml_ids(self):
        for id in self.employee_xml_ids:
            id.unlink()
        self.action_generate_line_xml()


    @api.depends('invoice_concept_ids')
    def _get_amount_total(self):
        self.amount_total_ret = 0.0
        for line in self.invoice_concept_ids:
            self.amount_total_ret += line.raw_tax_ut

    @api.depends('invoice_concept_ids')
    def _get_amount_total_base(self):
        self.amount_total_base = 0.0
        for line in self.invoice_concept_ids:
            self.amount_total_base += line.base_amount

    name = fields.Char(
        string='Descripción', size=128, required=True, select=True,
        default='Retención de ingresos ' + time.strftime('%m/%Y'),
        help="Descripción de la declaración de retención de ingresos")
    company_id = fields.Many2one(
        'res.company', string='Compañia', required=True,
        default=lambda self: self.env.company.id,
        help="Compañia")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('generated', 'Generado'),
        ('confirmed', 'Confirmado'),
        ('done', 'Realizado'),
        ('cancel', 'Cencelado')
    ], string='Estado', readonly=True, default='draft',
        help="Estado del Vale")
    amount_total_ret = fields.Float(
        compute='_get_amount_total', method=True, digits=(16, 2), readonly=True,
        string='Total de retención de ingresos',
        help="Importe total de la retención")
    amount_total_base = fields.Float(
        compute='_get_amount_total_base', method=True, digits=(16, 2), readonly=True,
        string='Sin cantidad de impuestos', help="Total sin impuestos")
    xml_ids = fields.One2many(
        'islr.xml.wh.line', 'islr_xml_wh_doc', 'Líneas de documentos XML',
        readonly=True, states={'draft': [('readonly', False)]},
        help='ID de línea de factura de retención XML')

    invoice_concept_ids = fields.One2many(
        'islr.wh.doc.line', 'islr_xml_wh_doc_id', 'Líneas de documentos XML',
        readonly=True, states={'draft': [('readonly', False)]},
        domain=[('type', '=', 'invoice')])

    employee_xml_ids = fields.One2many(
        'islr.xml.wh.line', 'islr_xml_wh_doc', 'Líneas de documentos XML',
        readonly=True, states={'draft': [('readonly', False)]},
        help='ID de línea de empleado de retención XML',
        domain=[('type', '=', 'employee')])
    user_id = fields.Many2one(
        'res.users', string='Usuario', readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user,
        help='Usuario que crea el documento')
    # rsosa: ID 95
    xml_filename = fields.Char('Nombre Archivo XML')
    xml_binary = fields.Binary('Archivo XML')

    date_start = fields.Date("Fecha Inicio", required=True,
                             states={'draft': [('readonly', False)]},
                             help="Begin date of period")
    date_end = fields.Date("fecha Fin", required=True,
                           states={'draft': [('readonly', False)]},
                           help="Begin date of period")

    def copy(self, default=None):
        """ Initialized id by duplicating
        """
        if default is None:
            default = {}
        default = default.copy()
        default.update({
            'xml_ids': [],
            'invoice_concept_ids': [],
            'employee_xml_ids': [],
        })

        return super(IslrXmlWhDoc, self).copy(default)

    def get_period(self):

        split_date = str(self.date_end).split('-')

        return str(split_date[0]) + str(split_date[1])

    def name_get(self):
        """ Return id and name of all records
        """
        context = self._context or {}
        if not len(self.ids):
            return []

        res = [(r['id'], r['name']) for r in self.read(
            ['name'])]
        return res

    def action_anular1(self):
        return self.write({'state': 'draft', 'xml_binary': False})

    def action_confirm1(self):
        return self.write({'state': 'confirmed'})

    def action_generate_line_xml(self):
        self.invoice_concept_ids = [(5, 0, 0)]
        concept_lines = self.env['islr.wh.doc'].search([('date_ret', '>=', self.date_start),
                                                        ('date_ret', '<=', self.date_end),
                                                        ('state', '=', 'confirmed'),
                                                        ('type', 'in', ['in_invoice', 'in_refund']),
                                                        ('company_id', '=', self.company_id.id)]).concept_ids.filtered(
            lambda l: not l.islr_xml_wh_doc_id)
        for line in self.employee_xml_ids:
            concept_lines += line.islr_wh_doc_line_id
        self.invoice_concept_ids = concept_lines

    def action_done1(self):

        root = self._xml()
        self._write_attachment(root)
        self.write({'state': 'done'})
        return True

    @api.model
    def _write_attachment(self, root):
        """ Codify the xml, to save it in the database and be able to
        see it in the client as an attachment
        @param root: data of the document in xml
        """
        fecha = time.strftime('%Y_%m_%d_%H%M%S')
        name = 'ISLR_' + fecha + '.' + 'xml'
        #         self.env('ir.attachment').create(cr, uid, {
        #             'name': name,
        #             'datas': base64.encodestring(root),
        #             'datas_fname': name,
        #             'res_model': 'islr.xml.wh.doc',
        #             'res_id': ids[0],
        #         }, context=context
        #         )
        #         cr.commit()
        # rsosa: ID 95
        self.write({
            'xml_filename': name,
            'xml_binary': base64.encodebytes(root)
        })
        # self.log( self.ids[0], _("File XML %s generated.") % name)

    @api.model
    def indent(self, elem, level=0):
        """ Return indented text
        @param level: number of spaces for indentation
        @param elem: text to indentig
        """
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def import_xml_employee(self):
        ids = isinstance(self.ids, (int)) and [self.ids] or self.ids
        xml_brw = self.browse(ids)[0]
        return {'name': _('Import XML employee'),
                'type': 'ir.actions.act_window',
                'res_model': 'employee.income.wh',
                'view_type': 'form',
                'view_id': False,
                'view_mode': 'form',
                'nodestroy': True,
                'target': 'new',
                'domain': "",
                'context': {
                    # 'default_period_id': xml_brw.period_id.id,
                    # 'islr_xml_wh_doc_id': xml_brw.id,
                    # 'period_code': "%0004d%02d" % (
                    #    period.tm_year, period.tm_mon),
                    'company_vat': xml_brw.company_id.partner_id.rif[0:]}}

    def _xml(self):
        """ Transform this document to XML format
        """
        rp_obj = self.env['res.partner']
        inv_obj = self.env['account.move']
        root = ''
        for ixwd_id in self.ids:
            wh_brw = self.browse(ixwd_id)

            period = self.get_period()
            company_vat = rp_obj._find_accounting_partner(wh_brw.company_id.partner_id).rif[0:]
            company_vat = company_vat.replace("-", "")
            company_vat1 = wh_brw.company_id.partner_id.rif
            company_vat1 = company_vat1.replace("-", "")
            root = Element("RelacionRetencionesISLR")
            x1 = "RifAgente"
            x2 = "Periodo"
            root.attrib[x1] = company_vat if company_vat1 else ''
            root.attrib[x2] = period

            partners = list(map(lambda xml_line: xml_line.partner_id, self.invoice_concept_ids))
            partners = list(set(partners))

            partners_person_pnre = list(filter(lambda partner: partner.people_type_individual == "pnre", partners))

            file_lines = {}

            for line in self.invoice_concept_ids:
                control_number = line.control_number.replace("-", "") if line.control_number else ""
                invoice_number = line.invoice_number if line.invoice_number else line.invoice_id.supplier_invoice_number
                partner_vat = line.partner_id.rif
                date_ret = line.islr_wh_doc_id.date_ret if line.islr_wh_doc_id else datetime.datetime.today()
                rate_id = line.concept_id.rate_ids.filtered(lambda this: this.name.lower() == line.partner_id.people_type_individual or this.name.lower() == line.partner_id.people_type_company)
                concept_code = rate_id.code
                base = line.base_amount
                percent = line.retencion_islr

                if invoice_number.find("-") != -1:
                    primeraLetraGuion = False
                    while primeraLetraGuion == False:
                        if invoice_number[0] == "-":
                            primeraLetraGuion = True
                        invoice_number = invoice_number[1:]
 
                if invoice_number.isdigit():
                    invoice_number_format = invoice_number
                else:
                    invoice_number_format = ""
                    for char in invoice_number:
                        if char.isdigit():
                            invoice_number_format += char

                if control_number.isdigit():
                    control_number_format = control_number
                else:
                    control_number_format = ""
                    for char2 in control_number:
                        if char2.isdigit():
                            control_number_format += char2

                if line.partner_id in partners_person_pnre:
                    if file_lines.get(partner_vat + concept_code, False):
                        file_lines[partner_vat + concept_code][5] += base
                    else:
                        file_lines[partner_vat + concept_code] = [partner_vat, invoice_number_format,
                                                                  control_number_format,
                                                                  date_ret.strftime('%d/%m/%Y'),
                                                                  concept_code, base, percent]
                else:
                    file_lines[invoice_number_format + concept_code] = [partner_vat, invoice_number_format,
                                                                        control_number_format,
                                                                        date_ret.strftime('%d/%m/%Y'),
                                                                        concept_code, base, percent]

            for index, value in file_lines.items():
                detalle = SubElement(root, "DetalleRetencion")
                SubElement(detalle, "RifRetenido").text = value[0]
                SubElement(detalle, "NumeroFactura").text = value[1]
                SubElement(detalle, "NumeroControl").text = value[2]
                SubElement(detalle, "FechaOperacion").text = value[3]
                SubElement(detalle, "CodigoConcepto").text = value[4]
                SubElement(detalle, "MontoOperacion").text = str(round(value[5],2))
                SubElement(detalle, "PorcentajeRetencion").text = str(value[6])

        return tostring(root, encoding="ISO-8859-1")


IslrXmlWhDoc()


class IslrXmlWhLine(models.Model):
    _name = "islr.xml.wh.line"
    _description = 'Generate XML Lines'

    concept_id = fields.Many2one(
        'islr.wh.concept', string='Concepto de Retencion',
        help="Concepto de retención asociado a esta tasa",
        required=True)
    partner_vat = fields.Char(
        'RIF', required=True, help="Socio RIF",  related="partner_id.rif", store="True")
    invoice_number = fields.Char(
        'Número de factura', size=20, required=True,
        default='0',
        help="Número de factura")
    control_number = fields.Char(
        'Numero de Control', size=20,
        default='NA',
        help="Reference")
    concept_code = fields.Char(
        'Código Conceptual', size=10, required=True, help="Código Conceptual")
    base = fields.Float(
        'Cantidad base', required=True,
        help="Amount where a withholding is going to be computed from",
        digits=dp.get_precision('Withhold ISLR'))
    raw_base_ut = fields.Float(
        'Cantidad de UT', digits=dp.get_precision('Withhold ISLR'),
        help="Cantidad de UT")
    raw_tax_ut = fields.Float(
        'Impuesto retenido de UT',
        digits=dp.get_precision('Withhold ISLR'),
        help="Impuesto retenido de UT")
    porcent_rete = fields.Float(
        'Porcentaje de retención', required=True, help="Porcentaje de retención",
        digits=dp.get_precision('Withhold ISLR'))
    wh = fields.Float(
        'Cantidad retenida', required=True,
        help="Cantidad retenida a socio",
        digits=dp.get_precision('Withhold ISLR'))
    rate_id = fields.Many2one(
        'islr.rates', 'Tipo de persona',
        domain="[('concept_id','=',concept_id)]", required=False,
        help="Tipo de persona")
    islr_wh_doc_line_id = fields.Many2one(
        'islr.wh.doc.line', 'Documento de retención de ingresos',
        ondelete='cascade', help="Documento de retención de ingresos")
    account_invoice_line_id = fields.Many2one(
        'account.move.line', 'Línea de factura',
        help="Línea de factura a retener")
    account_invoice_id = fields.Many2one(
        'account.move', 'Factura', help="Factura para Retener")
    islr_xml_wh_doc = fields.Many2one(
        'islr.xml.wh.doc', 'Documento XML ISLR', help="Impuesto sobre la renta XML Doc")
    partner_id = fields.Many2one(
        'res.partner', 'Empresa', required=True,
        help="Socio objeto de retención")
    sustract = fields.Float(
        'Sustraendo', help="Subtrahend",
        digits=dp.get_precision('Withhold ISLR'))
    islr_wh_doc_inv_id = fields.Many2one(
        'islr.wh.doc.invoices', 'Factura retenida',
        help="Facturas retenidas")
    date_ret = fields.Date('Fecha de Operacion')
    type = fields.Selection(
        ISLR_XML_WH_LINE_TYPES,
        string='Tipo', required=True, readonly=False,
        default='invoice')
    company_id = fields.Many2one('res.company', string='Compañia', compute='get_company_id', store=True)
    _rec_name = 'partner_id'

    @api.depends('account_invoice_id')
    def get_company_id(self):
        for res in self:
            if res.account_invoice_id.company_id:
                res.company_id = res.account_invoice_id.company_id.id
            else:
                res.company_id = None

    def onchange_partner_vat(self, partner_id):
        """ Changing the partner, the partner_vat field is updated.
        """
        context = self._context or {}
        rp_obj = self.env['res.partner']
        acc_part_brw = rp_obj._find_accounting_partner(rp_obj.browse(
            partner_id))
        return {'value': {'partner_vat': acc_part_brw.rif[2:]}}

    def onchange_code_perc(self, rate_id):
        """ Changing the rate of the islr, the porcent_rete and concept_code fields
        is updated.
        """
        context = self._context or {}
        rate_brw = self.env['islr.rates'].browse(rate_id)
        return {'value': {'porcent_rete': rate_brw.wh_perc,
                          'concept_code': rate_brw.code}}


IslrXmlWhLine()


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    wh_xml_id = fields.Many2one('islr.xml.wh.line', string='XML Id', default=0, help="XML withhold line id")


AccountInvoiceLine()
