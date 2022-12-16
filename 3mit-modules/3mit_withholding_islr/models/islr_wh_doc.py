# coding: utf-8
# coding: utf-8
##############################################################################
import time
from odoo import fields, models
from odoo.exceptions import UserError

ISLR_XML_WH_LINE_TYPES = [('invoice', 'Invoice'), ('employee', 'Employee')]


class IslrWhDoc(models.Model):
    _name = "islr.wh.doc"
    _order = 'date_ret desc, number desc'
    _description = 'Document Income Withholding'
    _rec_name = 'name'

    move_id = fields.Many2one(
        'account.move', 'Entrada de diario', ondelete='restrict',
        readonly=True, help="Bono contable")

    amount_total_signed = fields.Many2one('account.move', string='campo')
    name = fields.Char(
        'Numero de Comprobante', size=64,
        required=True,
        help="Número de Comprobante de Retención")
    number = fields.Char(
        'Número de Retención', size=32, help="referencia del vale")
    number_comprobante = fields.Char(
        'Número de Comprobante de Retención', size=32, help="Número de Comprobante de Retención")

    invoice_id = fields.Many2one("account.move", string="Factura retenida")

    journal_id = fields.Many2one(
        'account.journal', 'Diario', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        help="Diario donde se registran los asientos contables")

    type = fields.Selection([
        ('out_invoice', 'Factura de cliente'),
        ('in_invoice', 'Factura de proveedor'),
        ('in_refund', 'Reembolso de la factura del proveedor'),
        ('out_refund', 'Reembolso de la factura del cliente'),
    ], string='Tipo', readonly=True,
        help="Tipo de referencia")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('cancel', 'Cancelado')
    ], string='Estado', readonly=True, default='draft',
        help="estado del vale")
    date_ret = fields.Date(
        'Fecha de contabilidad', readonly=True,
        states={'draft': [('readonly', False)]},
        help="Mantener vacío para usar la fecha actual")
    date_uid = fields.Date(
        'Fecha de retención', readonly=True,
        states={'draft': [('readonly', False)]}, help="Fecha del vale")
    account_id = fields.Many2one(
        'account.account', 'Cuenta',  # required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Cuenta por cobrar o cuenta por pagar de socio")

    partner_id = fields.Many2one(
        'res.partner', 'Compañia', readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        help="Socio objeto de retención")
    currency_id = fields.Many2one(
        'res.currency', 'Moneda', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        help="Diario donde se registran los asientos contables")
    company_id = fields.Many2one(
        'res.company', 'Compañia', required=True,
        default=lambda self: self.env.company,
        help="Compañia")
    amount_total_ret = fields.Float(store=True, string='Monto total',
                                    digits='Withhold ISLR',
                                    help="Importe total retenido")
    concept_ids = fields.One2many(
        'islr.wh.doc.line', 'islr_wh_doc_id', 'Concepto de retención de ingresos',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Concepto de retención de ingresos')
    islr_wh_doc_id = fields.One2many(
        'account.move', 'islr_wh_doc_id', 'Facturas',
        states={'draft': [('readonly', False)]},
        help='Se refiere al documento de retención de ingresos del impuesto generado en la factura')
    user_id = fields.Many2one(
        'res.users', 'Salesman', readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda s: s._uid,
        help="Vendor user")
    automatic_income_wh = fields.Boolean(
        string='Retención Automática de Ingresos',
        default=False,
        help='Cuando todo el proceso se verifique automáticamente, y si todo está bien, se configurará como hecho')

    # Método computado que retorna la empresa actual
    def _get_company(self):
        res_company = self.env['res.company'].search(
            [('id', '=', self.company_id.id)])
        return res_company

    # Método que genera el código de secuencia de cada retención
    def retencion_seq_get(self):
        local_number = self.env['ir.sequence'].next_by_code('islr.wh.doc')
        if local_number and self.date_ret:
            account_month = self.date_ret.split('-')[1]
            if not account_month == local_number[4:6]:
                local_number = local_number[:4] + \
                    account_month + local_number[6:]
        return local_number

    # Método para calcular todos los montos de retención y sustraendo de cada concepto
    def create_xml_lines(self):
        ut = self.env["l10n.ut"].search(
            [("date", "<=", self.invoice_id.date)], order='date DESC', limit=1)
        if self.partner_id.company_type == "person":
            type_partner = self.partner_id.people_type_individual.upper()
        else:
            type_partner = self.partner_id.people_type_company.upper()

        if self.partner_id.rif:
            rif = self.partner_id.rif.replace("-", "")
        else:
            rif = str()

        if self.invoice_id.move_type in ["in_invoice", "in_refund"]:
            invoice_number = self.invoice_id.supplier_invoice_number
        else:
            invoice_number = self.invoice_id.payment_reference

        for line in self.concept_ids:
            invoice_lines = self.env["account.move.line"].search(
                [("move_id", "=", self.invoice_id.id), ("concept_id", "=", line.concept_id.id)])
            xml_line = self.env["islr.rates"].search(
                [("concept_id", "=", line.concept_id.id), ("name", "=", type_partner)])
            concepts = []
            for invoice_line in invoice_lines:
                line.xml_ids = [(0, 0, {
                    "islr_wh_doc_line_id": line.id,
                    "partner_vat": rif[0:12],
                    "partner_id": self.partner_id.id,
                    "concept_code": xml_line.code,
                    "porcent_rete": xml_line.wh_perc,
                    "rate_id": xml_line.id,
                    "concept_id": line.concept_id.id,
                    "account_invoice_line_id": invoice_line.id,
                    "control_number": self.invoice_id.nro_ctrl,
                    "invoice_number": invoice_number,
                    "base": - abs(invoice_line.price_subtotal_conversion) if self.invoice_id.move_type in ["in_refund", "out_refund"] else abs(invoice_line.price_subtotal_conversion),
                    "wh": invoice_line.price_subtotal_conversion * xml_line.wh_perc / 100,
                    "raw_base_ut": ut.amount,
                    "raw_tax_ut": invoice_line.price_subtotal_conversion * xml_line.wh_perc / 100,
                })]
                line.base_amount += invoice_line.price_subtotal_conversion
                line.amount += invoice_line.price_subtotal_conversion * xml_line.wh_perc / 100
                line.control_number = line.invoice_id.nro_ctrl
                if type_partner == "PNRE" and line.concept_id.id not in concepts:
                    line.subtract += round(ut.amount *
                                           xml_line.minimum * (xml_line.wh_perc / 100), 2)
                    concepts.append(line.concept_id.id)
            if line.invoice_id.move_type in ["in_invoice", "in_refund"]:
                invoice_number = line.invoice_id.supplier_invoice_number
            else:
                invoice_number = line.invoice_id.payment_reference
            line.invoice_number = invoice_number
            line.partner_vat = self.partner_id.rif
            line.partner_id = self.partner_id.id
            line.raw_base_ut = ut.amount
            line.retencion_islr = xml_line.wh_perc
            line.raw_tax_ut = line.amount - line.subtract
            if line.retention_rate != 0.0:
                line.currency_base_amount = line.base_amount / line.retention_rate
                line.currency_amount = line.amount / line.retention_rate
            self.amount_total_ret += line.raw_tax_ut

    # Método para crear líneas de concepto y XML cuando se crea una retención
    def create_islr_lines(self):
        concepts = self.invoice_id.get_islr_concepts()
        for concept in concepts:
            self.concept_ids = \
                [(0, 0, {
                    "concept_id": concept.id,
                    "invoice_id": self.invoice_id.id,
                    "retention_rate": self.invoice_id.currency_bs_rate,
                })]
        self.create_xml_lines()

    # Método para confirmar una retención
    def action_confirm(self):
        for ret in self:
            ret.action_number()
            # Se restringe la creación del asiento contable a facturas de clientes.
            if ret.invoice_id.move_type in ["out_refund", "out_invoice"]:
                ret.move_id = ret.action_move_create()
            ret.write({'state': 'confirmed'})
            ret.invoice_id.status = 'pro'

    # Método para eliminar líneas XML y de concepto al momento de cancelar la retención
    def action_cancel_process(self):
        line_obj = self.env['islr.wh.doc.line']
        inv_obj = self.env['account.move']
        wh_doc_id = self.id

        # Eliminar líneas XML y líneas de concepto
        islr_lines = line_obj.search([('islr_wh_doc_id', '=', wh_doc_id)])
        for islr_line in islr_lines:
            for xml_line in islr_line.xml_ids:
                xml_line.unlink()
            islr_line.unlink()

        # Actualizar información en factura
        inv_list = inv_obj.search([('islr_wh_doc_id', '=', wh_doc_id)])
        inv_list.write({'status': 'no_pro'})
        inv_list.write({'islr_wh_doc_id': False})

    def _get_sequence_code(self):
        self.invoice_ids.invoice_id.ensure_one()
        SEQUENCE_CODE = 'number_comprobante_islr'
        company_id = self._get_company()
        IrSequence = self.env['ir.sequence'].with_context(
            force_company=company_id.id)
        number = IrSequence.next_by_code(SEQUENCE_CODE)
        return number

    def action_number(self, *args):
        if self.type == 'in_invoice':
            for (iwd_id, number) in self._cr.fetchall():
                if not self.number:
                    number = self._get_sequence_code()
                    if not number:
                        raise UserError(
                            "Error Configuracion \nSin secuencia configurada para retención de ingresos del proveedor")

                    self.write({'number': number})
        else:
            for (iwd_id, number) in self._cr.fetchall():
                if not number:
                    number = self.env['ir.sequence'].get(
                        'islr.wh.doc.%s' % self.type)
                    if not number:
                        raise UserError(
                            "Falta la configuración! \nSin secuencia configurada para ingresos del proveedor Retenciones")
        return True

    # Método para cancelar una retención
    def action_cancel(self):
        # Se evaluan los archivos XMl asociados con esta retencion
        self._check_xml_wh_lines
        # Se realiza el asiento de reversion (en caso de facturas cliente)
        self.cancel_move()
        # Se eliminan las líneas XML, las líneas de retención y se actualiza la factura
        self.action_cancel_process()

        self.write({'state': 'cancel', 'automatic_income_wh': False})

    # Método para crear un asiento de reversión al cancelar la retención
    def cancel_move(self):
        for ret in self:
            if ret.state == 'confirmed':
                ref_move = ret.move_id._reverse_moves(
                    [{'date': self.date_ret}], cancel=True)
                ref_move.write({'ref': 'Reversión de ' + str(self.name) +
                               ' para la ' + str(self.invoice_id.name)})

    # Método para crear la entrada de diario cuando se confirma la retención
    def action_move_create(self):
        for ret in self:
            if ret.invoice_id.move_type in ('in_invoice', 'in_refund'):
                self.write({'date_ret': ret.date_ret})
            else:
                self.write({'date_ret': time.strftime('%Y-%m-%d')})

            journal_id = ret.journal_id.id
            name = 'COMP. RET. ISLR ' + ret.name + \
                ' Doc. ' + (ret.invoice_id.name or '')
            amount = self.amount_total_ret

            move = {'ref': name + 'de ' + str(ret.invoice_id.name),
                    'journal_id': journal_id,
                    'date': ret.date_ret,
                    'state': 'draft',
                    'type_name': 'entry',
                    'currency_id': self.env.company.currency_id.id,
                    'currency_bs_rate': ret.invoice_id.currency_bs_rate
                    }

            move_id = self.env['account.move'].create(move)
            if ret.invoice_id.move_type in ["out_invoice", "in_invoice"]:
                l1 = {
                    'account_id': ret.account_id.id,
                    'currency_id': self.env.company.currency_id.id,
                    'ref': ret.invoice_id.name,
                    'date': ret.date_ret,
                    'partner_id': ret.partner_id.commercial_partner_id.id,
                    'move_id': move_id.id,
                    'name': name,
                    'debit': abs(amount),
                    'credit': False,
                    'amount_currency': abs(amount),
                }
            else:
                l1 = {
                    'account_id': ret.account_id.id,
                    'currency_id': self.env.company.currency_id.id,
                    'ref': ret.invoice_id.name,
                    'date': ret.date_ret,
                    'partner_id': ret.partner_id.commercial_partner_id.id,
                    'move_id': move_id.id,
                    'name': name,
                    'debit': False,
                    'credit': abs(amount),
                    'amount_currency': - abs(amount),
                }

            acc = ret.journal_id.default_islr_account.id
            acc_part_id = ret.partner_id.commercial_partner_id.id
            if not acc:
                raise UserError(
                    "Falta la cuenta en el impuesto! \nEl diario de [%s] tiene las cuentas faltantes. Por favor, rellene los campos que faltan para poder continuar" % (
                        ret.journal_id.name))

            if ret.invoice_id.move_type in ["out_invoice", "in_invoice"]:
                l2 = {
                    'amount_currency': - abs(l1["amount_currency"]),
                    'debit': False,
                    'credit': l1["debit"],
                    'account_id': acc,
                    'partner_id': acc_part_id,
                    'ref': self.display_name,
                    'date': ret.date_ret,
                    'move_id': move_id.id,
                    'currency_id': self.env.company.currency_id.id,
                    'name': name.strip() + ' - ISLR: ' + ret.name.strip()
                }
            else:
                l2 = {
                    'amount_currency': abs(l1["amount_currency"]),
                    'debit': l1["credit"],
                    'credit': False,
                    'account_id': acc,
                    'partner_id': acc_part_id,
                    'ref': self.display_name,
                    'date': ret.date_ret,
                    'move_id': move_id.id,
                    'currency_id': self.env.company.currency_id.id,
                    'name': name.strip() + ' - ISLR: ' + ret.name.strip()
                }

            self.env['account.move.line'].with_context(
                check_move_validity=False).create(l1)
            self.env['account.move.line'].with_context(
                check_move_validity=False).create(l2)

            move_id.post()
            for line in ret.concept_ids:
                for xml_line in line.xml_ids:
                    xml_line.date_ret = ret.date_ret

            return move_id

    # Método para verificar una retención próxima a eliminarse
    def unlink(self):
        for islr_brw in self:
            if islr_brw.state != 'cancel':
                raise UserError(
                    "El documento de retención debe estar en estado cancelado para ser eliminado.")
            else:
                return super(IslrWhDoc, self).unlink()

    # Método para verificar archivos XML asociados a una retención ISLR próxima a cancelarse
    def _check_xml_wh_lines(self):
        for concept in self.concept_ids:
            for line in concept.xml_ids:
                if line.islr_xml_wh_doc:
                    if line.islr_xml_wh_doc.state != 'draft':
                        raise UserError("Error!! El siguiente archivo XML debe establecerse en Borrador antes de Cancelar este documento %s" % (
                            line.islr_xml_wh_doc.name))


class IslrWhDocLine(models.Model):
    _name = "islr.wh.doc.line"
    _description = 'Lines of Document Income Withholding'

    name = fields.Char(
        'Descripción', size=64, help="Description of the voucher line")
    invoice_id = fields.Many2one(
        'account.move', 'Factura', ondelete='set null',
        help="Factura para Retener")
    control_number = fields.Char(string="Número de control")
    invoice_number = fields.Char(string="Número de factura")
    amount = fields.Float(string='Cantidad retenida', digits=(
        16, 2), help="Monto retenido del monto base")
    currency_amount = fields.Float(method=True, digits=(16, 2),
                                   string='Moneda retenida Monto retenido', multi='all',
                                   help="Monto retenido del monto base")
    base_amount = fields.Float(
        'Cantidad base', digits='Withhold ISLR',
        help="Cantidad base")
    currency_base_amount = fields.Float(method=True, digits=(16, 2),
                                        string='Monto base en moneda extranjera', multi='all',
                                        help="Monto retenido del monto base")
    raw_base_ut = fields.Float(
        'Cantidad de UT', digits='Withhold ISLR',
        help="Cantidad de UT")
    raw_tax_ut = fields.Float(
        'Impuesto retenido de UT',
        digits='Withhold ISLR',
        help="Impuesto retenido de UT")
    subtract = fields.Float(
        'Sustraer', digits='Withhold ISLR',
        help="Sustraer")
    islr_wh_doc_id = fields.Many2one(
        'islr.wh.doc', 'Retener documento', ondelete='cascade',
        help="Retención de documentos del impuesto sobre la renta generado por esta factura")
    islr_xml_wh_doc_id = fields.Many2one(
        'islr.xml.wh.doc', 'Archivo XML', ondelete='set null',
        help="Retención de documentos del impuesto sobre la renta generado por esta factura")
    type = fields.Selection(
        ISLR_XML_WH_LINE_TYPES,
        string='Tipo', required=True, readonly=False,
        default='invoice')
    concept_id = fields.Many2one(
        'islr.wh.concept', 'Concepto de retención',
        help="Concepto de retención asociado a esta tasa")
    retencion_islr = fields.Float(
        'Porcentaje de retención',
        digits='Withhold ISLR',
        help="Tasa de retención")
    retention_rate = fields.Float(default=0, method=True, string='Tasa de retención',
                                  help="Withhold rate has been applied to the invoice",
                                  digits='Withhold ISLR')
    xml_ids = fields.One2many(
        'islr.xml.wh.line', 'islr_wh_doc_line_id', 'XML Lines',
        help='ID de línea de factura de retención XML')
    iwdi_id = fields.Many2one(
        'islr.wh.doc.invoices', 'Factura retenida', ondelete='cascade',
        help="Facturas retenidas")
    partner_id = fields.Many2one('res.partner', string='Partner', store=True)
    partner_vat = fields.Char(string="RIF")
    fiscalyear_id = fields.Many2one(
        'account.fiscalyear', string='Fiscalyear', store=True)
    company_id = fields.Many2one(
        'res.company', 'Compañia', required=True,
        default=lambda self: self.env.company,
        help="Compañia")
