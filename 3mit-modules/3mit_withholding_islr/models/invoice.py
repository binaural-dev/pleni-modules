# coding: utf-8
##############################################################################
from odoo import api
from odoo import fields, models
from odoo.exceptions import UserError
from collections import defaultdict
from odoo.tools.misc import formatLang

class AccountTipeTax(models.Model):
    _inherit = 'account.tax'

    type_tax = fields.Selection([('iva', 'IVA'),
                                 ('iva_ret', 'RETENCION IVA'),
                                 ('islr_ret', 'RETENCION ISLR')
                                 ], help="Selecione el Tipo de Impuesto",
                                string="Tipo de Impuesto", groups="3mit_grupo_localizacion.group_localizacion")

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    apply_wh = fields.Boolean(
        string='Withheld', default=False, groups="3mit_grupo_localizacion.group_localizacion",
        help="Indicates whether a line has been retained or not, to"
             " accumulate the amount to withhold next month, according"
             " to the lines that have not been retained.")
    concept_id = fields.Many2one('islr.wh.concept', 'Concepto de Islr', groups="3mit_grupo_localizacion.group_localizacion",
                                 help="concepto de retención de ingresos asociada a esta tasa",
                                 default=lambda self: self.env['islr.wh.concept'].search(
                                     [('name', '=', 'NO APLICA RETENCION')]))
    state = fields.Selection([('draft', 'Draft'),
                              ('open', 'Open'),
                              ('paid', 'Paid'),
                              ('cancel', 'Cancelled'),
                              ], index=True, readonly=True, default='draft', track_visibility='onchange', copy=False, groups="3mit_grupo_localizacion.group_localizacion",
                             help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
                                  " * The 'Pro-forma' status is used when the invoice does not have an invoice number.\n"
                                  " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
                                  " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
                                  " * The 'Cancelled' status is used when user cancel invoice.")

    @api.onchange('concept_id')
    def _onchange_concept_id(self):
        for line in self:
            taxes = line.get_islr_tax()
            if taxes and line.move_id.fiscal_position_id:
                taxes = line.move_id.fiscal_position_id.map_tax(taxes, partner=line.partner_id)
            line.tax_ids += taxes


    def get_islr_tax(self):
        self.ensure_one()

        tax_ids = self.env['account.tax']
        if self.move_id.is_purchase_document(include_receipts=True):
            if self.move_id.partner_id.islr_withholding_agent and self.concept_id:
                if self.concept_id.id != 1:
                    tax_ids += self.move_id.partner_id.tax_islr
        return tax_ids

class AccountMove(models.Model):
    _inherit = 'account.move'

    islr_wh_doc_id = fields.Many2one(
        'islr.wh.doc', string='Comprobante de retención de ingresos', ondelete='cascade', copy=False, groups="3mit_grupo_localizacion.group_localizacion",
        help="Documentación de la retención de ingresos del impuesto generado a partir de esta factura")

    status = fields.Selection([
            ('pro', 'Retención procesada, línea xml generada'),
            ('no_pro', 'Retención no procesada'),
            ('tasa', 'No exceda la tasa, línea xml generada'),
            ], string='Status', readonly=True, default='no_pro', copy=False, groups="3mit_grupo_localizacion.group_localizacion",
            help=''' * La \'Retención procesada, línea xml generada\'
            es usada cuando el usuario procesa la Retencion de ISLR.
            * La 'Retencion no Procesada\' state es cuando un usuario realiza una factura y se genera el documento de retencion de islr y aun no esta procesado.
            * \'No exceda la tasa, línea XML generada\' se utiliza cuando el usuario crea la factura, una factura no supera la tarifa mínima.''')

    # METODO PARA CALCULAR EL IMPUESTO ISLR
    def calculate_islr_tax(self):
        for invoice in self:
            islr_impuesto_total = 0
            num = 0
            # Se evalua si el partner retiene ISLR, si tiene impuesto islr asociado y si es una factura de proveedor
            if invoice.partner_id.tax_islr and invoice.partner_id.islr_withholding_agent and invoice.move_type in ["in_refund", "in_invoice"]:
                # Se calcula el impuesto ISLR de la factura
                ut = invoice.env["l10n.ut"].search([("date", "<=", invoice.date)], order='date DESC', limit=1)
                concepts = []
                for line in invoice.invoice_line_ids:
                    if line.concept_id:
                        if line.concept_id.name != "NO APLICA RETENCION":
                            num += 1
                            for rate in line.concept_id.rate_ids:
                                minimum = 0
                                if invoice.partner_id.company_type == "person":
                                    if rate.name == invoice.partner_id.people_type_individual.upper():
                                        minimum = rate.minimum
                                        islr_impuesto_total -= (line.price_subtotal * rate.wh_perc) / 100
                                        if line.concept_id.id not in concepts and invoice.partner_id.people_type_individual.upper() == "PNRE":
                                            islr_impuesto_total += (ut.amount * minimum * (rate.wh_perc / 100))/line.move_id.currency_bs_rate if line.move_id.currency_id.name == "USD" else (ut.amount * minimum * (rate.wh_perc / 100))
                                            concepts.append(line.concept_id.id)
                                if invoice.partner_id.company_type == "company":
                                    if rate.name == invoice.partner_id.people_type_company.upper():
                                        islr_impuesto_total -= (line.price_subtotal * rate.wh_perc) / 100

            if num != 0.0:
                return islr_impuesto_total/num
            else:
                return 0

    def get_islr_concepts(self):
        concepts = []
        for line in self.invoice_line_ids:
            if line.concept_id:
                if line.concept_id.name != "NO APLICA RETENCION" and line.concept_id not in concepts:
                    concepts.append(line.concept_id)
        return concepts

    def make_retention(self):
        if self.partner_id.islr_withholding_agent:
            # Elimina la retención anterior
            if self.islr_wh_doc_id:
                ret_islr = self.islr_wh_doc_id
                self.islr_wh_doc_id.action_cancel()
                ret_islr.unlink()

            # Se crea una nueva retención
            concepts = self.get_islr_concepts()
            if len(concepts) > 0:
                if self.state == 'posted':
                    self._create_islr_wh_doc()
                if self.state == 'draft':
                    self.action_post()

    @api.model
    def _create_islr_wh_doc(self):
        # Cargar parametros iniciales de la retención ISLR
        cod_retention = self.env['islr.wh.doc'].retencion_seq_get()
        partner_id = self.partner_id.commercial_partner_id
        automatic_retention = False
        if self.company_id.automatic_income_wh:
            automatic_retention = True
        if self.move_type in ('out_invoice', 'out_refund'):
            if partner_id.property_account_receivable_id:
                acc_id = partner_id.property_account_receivable_id.id
            else:
                raise UserError("El usuario %s no tiene una cuenta a cobrar configurada" % self.partner_id.name)
            if self.partner_id.sale_islr_journal_id:
                journal = self.partner_id.sale_islr_journal_id
            else:
                raise UserError("El usuario %s no tiene un diario de retención configurado" % self.partner_id.name)
        else:
            if partner_id.property_account_payable_id.id:
                acc_id = partner_id.property_account_payable_id.id
            else:
                raise UserError("El usuario %s no tiene una cuenta a pagar configurada" % self.partner_id.name)
            if self.partner_id.purchase_islr_journal_id:
                journal = self.partner_id.purchase_islr_journal_id
            else:
                raise UserError("El usuario %s no tiene un diario de retención configurado" % self.partner_id.name)


        values = {
            'name': cod_retention,
            'partner_id': partner_id.id,
            'account_id': acc_id,
            'type': self.move_type,
            'journal_id': journal.id,
            'company_id': self.company_id.id,
            'date_ret': self.date,
            'date_uid': self.date,
            'currency_id': self.company_id.currency_id.id,
            'automatic_income_wh': automatic_retention,
            'invoice_id': self.id,
        }

        retencion = self.env['islr.wh.doc'].create(values)
        retencion.create_islr_lines()
        self.islr_wh_doc_id = retencion.id

        # Confirmar automáticamente la retención (solo si la empresa fue configurada de tal forma)
        if self.islr_wh_doc_id.automatic_income_wh:
            self.islr_wh_doc_id.action_confirm()


# METODOS ESTANDAR DE ODOO SOBREESCRITOS O HEREDADOS --------------------------------------------
    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        ''' Compute the dynamic tax lines of the journal entry.

        :param lines_map: The line_ids dispatched by type containing:
            * base_lines: The lines having a tax_ids set.
            * tax_lines: The lines having a tax_line_id set.
            * terms_lines: The lines generated by the payment terms of the invoice.
            * rounding_lines: The cash rounding lines of the invoice.
        '''
        self.ensure_one()
        in_draft_mode = self != self._origin

        def _serialize_tax_grouping_key(grouping_dict):
            ''' Serialize the dictionary values to be used in the taxes_map.
            :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
            :return: A string representing the values.
            '''
            return '-'.join(str(v) for v in grouping_dict.values())

        def _compute_base_line_taxes(base_line):
            ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
            amount_currency & balance could not be the same as the expected currency rate.
            The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
            :param base_line:   The account.move.line owning the taxes.
            :return:            The result of the compute_all method.
            '''
            move = base_line.move_id

            if move.is_invoice(include_receipts=True):
                handle_price_include = True
                sign = -1 if move.is_inbound() else 1
                quantity = base_line.quantity
                is_refund = move.move_type in ('out_refund', 'in_refund')
                price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
            else:
                handle_price_include = False
                quantity = 1.0
                tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
                is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
                price_unit_wo_discount = base_line.amount_currency

            balance_taxes_res = base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                price_unit_wo_discount,
                currency=base_line.currency_id,
                quantity=quantity,
                product=base_line.product_id,
                partner=base_line.partner_id,
                is_refund=is_refund,
                handle_price_include=handle_price_include,
            )

            total_tax_amount = 0
            for line in balance_taxes_res["taxes"]:
                if line["name"] == "Retención ISLR Compras":
                    line["amount"] = self.calculate_islr_tax()
                total_tax_amount += line["amount"]

            balance_taxes_res["total_included"] = balance_taxes_res["total_excluded"] + total_tax_amount

            if move.move_type == 'entry':
                repartition_field = is_refund and 'refund_repartition_line_ids' or 'invoice_repartition_line_ids'
                repartition_tags = base_line.tax_ids.flatten_taxes_hierarchy().mapped(repartition_field).filtered(lambda x: x.repartition_type == 'base').tag_ids
                tags_need_inversion = self._tax_tags_need_inversion(move, is_refund, tax_type)
                if tags_need_inversion:
                    balance_taxes_res['base_tags'] = base_line._revert_signed_tags(repartition_tags).ids
                    for tax_res in balance_taxes_res['taxes']:
                        tax_res['tag_ids'] = base_line._revert_signed_tags(self.env['account.account.tag'].browse(tax_res['tag_ids'])).ids

            return balance_taxes_res

        taxes_map = {}

        # ==== Add tax lines ====
        to_remove = self.env['account.move.line']
        for line in self.line_ids.filtered('tax_repartition_line_id'):
            grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
            grouping_key = _serialize_tax_grouping_key(grouping_dict)
            if grouping_key in taxes_map:
                # A line with the same key does already exist, we only need one
                # to modify it; we have to drop this one.
                to_remove += line
            else:
                taxes_map[grouping_key] = {
                    'tax_line': line,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                }
        if not recompute_tax_base_amount:
            self.line_ids -= to_remove

        # ==== Mount base lines ====
        for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
            # Don't call compute_all if there is no tax.
            if not line.tax_ids:
                if not recompute_tax_base_amount:
                    line.tax_tag_ids = [(5, 0, 0)]
                continue

            compute_all_vals = _compute_base_line_taxes(line)

            # Assign tags on base line
            if not recompute_tax_base_amount:
                line.tax_tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

            tax_exigible = True
            for tax_vals in compute_all_vals['taxes']:
                grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
                grouping_key = _serialize_tax_grouping_key(grouping_dict)

                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

                if tax.tax_exigibility == 'on_payment':
                    tax_exigible = False

                taxes_map_entry = taxes_map.setdefault(grouping_key, {
                    'tax_line': None,
                    'amount': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                })
                taxes_map_entry['amount'] += tax_vals['amount']
                taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line, tax_vals['group'])
                taxes_map_entry['grouping_dict'] = grouping_dict
            if not recompute_tax_base_amount:
                line.tax_exigible = tax_exigible

        # ==== Pre-process taxes_map ====
        taxes_map = self._preprocess_taxes_map(taxes_map)

        # ==== Process taxes_map ====
        for taxes_map_entry in taxes_map.values():
            # The tax line is no longer used in any base lines, drop it.
            if taxes_map_entry['tax_line'] and not taxes_map_entry['grouping_dict']:
                if not recompute_tax_base_amount:
                    self.line_ids -= taxes_map_entry['tax_line']
                continue

            currency = self.env['res.currency'].browse(taxes_map_entry['grouping_dict']['currency_id'])

            # Don't create tax lines with zero balance.
            if currency.is_zero(taxes_map_entry['amount']):
                if taxes_map_entry['tax_line'] and not recompute_tax_base_amount:
                    self.line_ids -= taxes_map_entry['tax_line']
                continue

            # tax_base_amount field is expressed using the company currency.
            tax_base_amount = currency._convert(taxes_map_entry['tax_base_amount'], self.company_currency_id, self.company_id, self.date or fields.Date.context_today(self))

            # Recompute only the tax_base_amount.
            if recompute_tax_base_amount:
                if taxes_map_entry['tax_line']:
                    taxes_map_entry['tax_line'].tax_base_amount = tax_base_amount
                continue

            balance = currency._convert(
                taxes_map_entry['amount'],
                self.company_currency_id,
                self.company_id,
                self.date or fields.Date.context_today(self),
            )
            to_write_on_line = {
                'amount_currency': taxes_map_entry['amount'],
                'currency_id': taxes_map_entry['grouping_dict']['currency_id'],
                'debit': balance > 0.0 and balance or 0.0,
                'credit': balance < 0.0 and -balance or 0.0,
                'tax_base_amount': tax_base_amount,
            }

            if taxes_map_entry['tax_line']:
                # Update an existing tax line.
                taxes_map_entry['tax_line'].update(to_write_on_line)
            else:
                create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
                taxes_map_entry['tax_line'] = create_method({
                    **to_write_on_line,
                    'name': tax.name,
                    'move_id': self.id,
                    'partner_id': line.partner_id.id,
                    'company_id': line.company_id.id,
                    'company_currency_id': line.company_currency_id.id,
                    'tax_base_amount': tax_base_amount,
                    'exclude_from_invoice_tab': True,
                    'tax_exigible': tax.tax_exigibility == 'on_invoice',
                    **taxes_map_entry['grouping_dict'],
                })

            if in_draft_mode:
                taxes_map_entry['tax_line'].update(taxes_map_entry['tax_line']._get_fields_onchange_balance(force_computation=True))

    def action_post(self):
        res = super(AccountMove, self).action_post()
        # Solo retiene al CONFIRMAR cuando son facturas de cliente (out-invoice, out-refund)
        if self.move_type in ["out_refund", "out_invoice"]:
            self.make_retention()
        return res