# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError, Warning, ValidationError
from datetime import datetime, timedelta



class AccountAdvancePayment(models.Model):
    _name = 'account.advanced.payment'
    _description = 'Advance payments'

    ADVANCE_PAYMET_STATES = [('draft', 'Sin Publicar'),
                             ('cancel', 'Cancelado'),
                             ('available', 'Disponible'),
                             ('paid', 'Pagado')]

    name = fields.Char(string='Name')
    # name_apply = fields.Char(string='Name',default=lambda self: self.env['ir.sequence'].next_by_code('apply.advance.sequence'))
    supplier = fields.Boolean(string='Supplier')
    customer = fields.Boolean(string='Customer')
    company_currency = fields.Many2one('res.currency', string='Bs currency',
                                       default=lambda self: self.env.company.currency_id)
    partner_id = fields.Many2one('res.partner', string='Socio')
    bank_account_id = fields.Many2one('account.journal', string='Bank')
    advance_account_id = fields.Many2one('account.journal', string='Bank')
    payment_id = fields.Char(string='Payment Methods')
    date_advance = fields.Date(string='Advance Date')
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount_advance = fields.Monetary(string="Amount advance", currency_field='currency_id')
    ref = fields.Char(string= 'Referencia')
    move_id = fields.Many2one('account.move', 'Asiento contable')
    move_line = fields.One2many('account.move.line',
                                         related='move_id.line_ids',
                                         string='Asientos contables', readonly=True)
    move_apply_id = fields.Many2one('account.move', 'Asiento contable')
    move_apply_line = fields.One2many('account.move.line',
                                related='move_id.line_ids',
                                string='Asientos contables', readonly=True)
    move_refund_id = fields.Many2one('account.move', 'Asiento contable')
    move_refund_line = fields.One2many('account.move.line',
                                      related='move_id.line_ids',
                                      string='Asientos contables', readonly=True)
    state = fields.Selection(ADVANCE_PAYMET_STATES, string='Status',readonly=True, copy=False, default='draft')
    asiento_conciliado = fields.One2many('account.move.line', related='move_id.line_ids', string='Asientos contables', readonly=True)
    asiento_conl_apply = fields.One2many('account.move.line', related='move_apply_id.line_ids', string='Asientos contables',
                                         readonly=True)
    amount_available_conversion = fields.Monetary("Conversión Monto Disponible", currency_field='conversion_currency')
    amount_available = fields.Monetary("Amount Available", currency_field='currency_id')
    date_apply = fields.Date(string='Date apply')
    invoice_id = fields.Many2one('account.move',string='Invoice')
    invoice_currency = fields.Many2one('res.currency', related="invoice_id.currency_id")
    amount_invoice = fields.Monetary(string='Amount Invoice', currency_field='invoice_currency')
    conversion_currency = fields.Many2one('res.currency', string='Moneda de conversion', compute='_compute_conversion_currency')
    amount_currency_apply = fields.Many2one('res.currency', string='Moneda del monto', store=True)
    amount_apply = fields.Monetary(string='Amount Apply', currency_field='amount_currency_apply')
    is_customer = fields.Boolean("Is customer", default= True)
    is_supplier = fields.Boolean("Is Supplier", default=True)
    rate = fields.Float(digits=0, default=1.0, help='Tasa de registro del anticipo')
    tasa_anticipo = fields.Many2one('res.currency.rate', string='Tasa con la que se registró el anticipo')
    type_advance = fields.Boolean(default=False)
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )
    amount_rate = fields.Monetary(string='Amount Rate', currency_field='company_currency')
    amount_rate_apply = fields.Monetary(string='Amount Rate apply', currency_field='company_currency')
    currency_id_bool = fields.Boolean(default=False)
    currency_apply_bool = fields.Boolean(default=False)

    def action_register_advance(self):
        # funcionalidad del boton validate este hace llamada a las fucniones que realizan los asientos contables'''
        if self.state == 'draft':
            self.validate_amount_advance()
            self.get_move_register()
            self.move_id.currency_bs_rate = self.amount_rate
        elif self.state == 'posted' or 'available':
            self.validate_amount_apply()
            self.resta_amount_available()
            self.get_move_apply()
            self.state = 'paid'
            self.move_apply_id.currency_bs_rate = self.amount_rate_apply
            if self.amount_available > 0:
                self.copy()
                self.state = 'paid'
                self.env['account.move'].search([('id', '=', self.invoice_id.id)]).write({'anticipo_ref': self.id})

    @api.depends('amount_currency_apply')
    def _compute_conversion_currency(self):
        usd_currency = self.env['res.currency'].search([('name', '=', 'USD')])
        if self.currency_id == self.env.company.currency_id:
            self.conversion_currency = usd_currency.id
        else:
            self.conversion_currency = self.env.company.currency_id.id

    def obtener_tasa(self):
        if self.date_apply:
            fecha = self.date_apply
        else:
            fecha = self.date_advance
        date = datetime.combine(fecha, datetime.min.time())
        date = date + timedelta(hours=27, minutes=59, seconds=59)
        currency = self.env['res.currency'].search([('name', '=', 'USD')], order='id desc', limit=1).id
        tasa = self.env['res.currency.rate'].search([('currency_id', '=', currency), ('name', '<=', date)], order='name desc', limit=1)
        if not tasa:
            raise UserError("Advertencia! \nNo hay referencia de tasas registradas para moneda USD en la fecha igual o inferior de la Generacion del anticipo %s" % (self.name))
        return tasa.rate_divided

    @api.onchange('date_advance')
    def onchange_date_advance(self):
        self.onchange_currency_id()

    @api.onchange('currency_id')
    def onchange_currency_id(self):
        if self.currency_id:
            self.amount_rate = self.obtener_tasa()
            self.amount_rate_apply = self.amount_rate

    def validate_amount_advance(self):
        if not self.amount_advance > 0:
            raise Warning(_('El monto de anticipo debe ser mayor que cero'))
        return True

    @staticmethod
    def validation_date(date):
        if not date:
            raise ValidationError('Establezca la fecha de aplicación')

    def calculo_amount_apply(self):
        if self.invoice_id:
            if self.invoice_id.currency_id == self.amount_currency_apply:
                self.amount_apply = self.amount_invoice
            else:
                if self.invoice_id.currency_id == self.env.company.currency_id:
                    self.amount_apply = self.amount_invoice / self.amount_rate_apply
                else:
                    self.amount_apply = self.amount_invoice * self.amount_rate_apply

    def calculo_amount_available_conversion(self):
        if self.currency_id == self.env.company.currency_id:
            self.amount_available_conversion = self.amount_available / self.amount_rate_apply
        else:
            self.amount_available_conversion = self.amount_available * self.amount_rate_apply

    @api.onchange('date_apply')
    def onchange_date_apply(self):
        self.onchange_currency_id_apply()

    @api.onchange('invoice_id')
    def onchange_bill_id(self):
        self.amount_invoice = self.invoice_id.amount_residual
        self.validation_date(self.date_apply)
        self.calculo_amount_apply()

    @api.onchange('amount_currency_apply')
    def onchange_currency_id_apply(self):
        self.validation_date(self.date_apply)
        self.amount_rate_apply = self.obtener_tasa()
        self.onchange_rate_apply()

    @api.onchange('amount_rate_apply')
    def onchange_rate_apply(self):
        self.calculo_amount_apply()
        self.calculo_amount_available_conversion()

    def validate_amount_apply(self):
        simbolo = self.amount_currency_apply.symbol
        if self.amount_currency_apply == self.invoice_id.currency_id:
            if self.amount_apply > self.amount_invoice:
                raise ValidationError(
                    f"El monto a aplicar ({self.amount_apply} {simbolo}) no puede ser mayor al monto de la factura ({self.amount_invoice} {simbolo})")
        else:
            if self.invoice_id.currency_id == self.env.company.currency_id:
                amount_invoice = round((self.amount_invoice / self.amount_rate_apply), 2)
            else:
                amount_invoice = round((self.amount_invoice * self.amount_rate_apply), 2)
            if self.amount_apply > amount_invoice:
                raise ValidationError(
                    f"El monto a aplicar ({self.amount_apply} {simbolo}) no puede ser mayor al monto de la factura ({amount_invoice} {simbolo})")
        if self.amount_currency_apply == self.currency_id:
            amount_available = self.amount_available
        else:
            amount_available = self.amount_available_conversion
        if self.amount_apply > amount_available:
            raise ValidationError(
                f"El monto a aplicar ({self.amount_apply} {simbolo}) no puede ser mayor al monto disponible ({amount_available} {simbolo})")

    def resta_amount_available(self):
        if self.amount_currency_apply == self.currency_id:
            self.amount_available = self.amount_available - self.amount_apply
        else:
            if self.amount_currency_apply == self.env.company.currency_id:
                self.amount_available = self.amount_available_conversion - self.amount_apply
                self.amount_available = self.amount_available / self.amount_rate_apply
            else:
                self.amount_available = self.amount_available_conversion - self.amount_apply
                self.amount_available = self.amount_available * self.amount_rate_apply

    def unlink(self):
        # convierte a borrador la vista para ser editada
        for move_id in self:
            if move_id.state not in ('draft','cancel'):
                raise Warning(_('You cannot delete an advance payment is not draft or cancelled'))
        return models.Model.unlink(self)

    def copy(self, default=None):
        # Duplica un nuevo anticipo con estado disponible si el monto disponible es diferente de cero
        if default is None:
            default = {}
        default = default.copy()
        # local_amount_available = self.amount_available-self.amount_apply
        if self.amount_available > 0:
            default.update({
                'name': self.name,
                'partner_id': self.partner_id.id,
                'invoice_id': None,
                'amount_advance': self.amount_advance,
                'amount_available': self.amount_available,
                'amount_apply': 0.0,
                'state':'available',
            })
        # Se crea una copia del anticipo cuando se cancela un anticipo que fue procesado completamente
        elif self.amount_available == 0 and self.state == 'paid':
            default.update({
                'name': self.name,
                'partner_id': self.partner_id.id,
                'invoice_id': None,
                'amount_advance': self.amount_advance,
                'amount_available': self.amount_available + self.amount_apply,
                'amount_apply': 0.0,
                'state': 'available',
            })

            #raise Warning(_('El monto a aplicar (%s) no puede ser mayor al monto disponible'))

        return super(AccountAdvancePayment, self).copy(default)

    @api.model
    def create(self, vals):
        self.company_id = self.env.company
        if vals.get('is_supplier') == True and self.partner_id.es_cliente == False:
            vals.update({'supplier': ((self.env['res.partner'].browse(vals['partner_id']).es_cliente) == False), 'is_customer': False})
            self.is_customer = False
        else:
            vals.update({'customer': self.env['res.partner'].browse(vals['partner_id']).es_cliente, 'is_supplier': False})
            self.is_supplier = False
        res = super(AccountAdvancePayment, self).create(vals)

        return res

    @api.model
    def get_account_advance(self):
        # obtiene la cuentas contables segun el proveedor o cliente, para el registro de los anticipos
        cuenta_acreedora = None
        cuenta_deudora = None
        partner_id = None
        sequence_code = None
        is_customer = None
        is_supplier = None

        # if self.is_customer and self.state == 'draft':
        if self.partner_id.es_cliente and self.state == 'draft' and self.type_advance == False:
            cuenta_deudora = self.bank_account_id.payment_debit_account_id.id if self.bank_account_id.payment_debit_account_id.id \
                else self.bank_account_id.extra2_account_id.id
            cuenta_acreedora = self.env.company.advance_account_sale_id.id
            partner_id = self.partner_id.id
            sequence_code = 'register.receivable.advance.customer'
            self.is_customer = True
            self.is_supplier = False

        # elif self.is_supplier and self.state == 'draft':
        elif self.partner_id.es_proveedor and self.state == 'draft' and self.type_advance:
            cuenta_deudora = self.env.company.advance_account_purchase_id.id
            cuenta_acreedora = self.bank_account_id.payment_credit_account_id.id if self.bank_account_id.payment_credit_account_id.id \
                else self.bank_account_id.extra2_account_id.id
            partner_id = self.partner_id.id
            sequence_code = 'register.payment.advance.supplier'
            self.is_supplier = True
            self.is_customer = False

        return cuenta_deudora,cuenta_acreedora,partner_id,sequence_code,is_supplier,is_customer

    def get_account_apply(self):
        # obtiene la cuentas contables segun el proveedor o cliente, para la aplicacion de los anticipos
        cuenta_acreedora = None
        cuenta_deudora = None

        if self.partner_id.es_cliente and self.state in ['posted', 'available', 'paid'] and self.type_advance == False:
            cuenta_deudora = self.env.company.advance_account_sale_id.id
            cuenta_acreedora = self.partner_id.property_account_receivable_id.id

        elif self.partner_id.es_proveedor and self.state in ['posted', 'available', 'paid'] and self.type_advance:
            cuenta_deudora = self.partner_id.property_account_payable_id.id
            cuenta_acreedora = self.env.company.advance_account_purchase_id.id

        return cuenta_deudora, cuenta_acreedora

    def get_account_refund(self):
        # obtiene la cuentas contables segun el proveedor o cliente, para el reintegro de monto residual de los anticipos
        cuenta_acreedora = None
        cuenta_deudora = None
        partner_id = None
        #sequence_code = None

        if self.partner_id.es_cliente and self.state == 'available' and self.type_advance == False:
            cuenta_deudora = self.env.company.advance_account_sale_id.id
            cuenta_acreedora = self.bank_account_id.payment_debit_account_id.id
            partner_id = self.partner_id.id
            #sequence_code = 'register.receivable.advance.customer'

        elif self.partner_id.es_proveedor and self.state == 'available' and self.type_advance:
            cuenta_deudora = self.bank_account_id.payment_credit_account_id.id
            cuenta_acreedora = self.env.company.advance_account_purchase_id.id
            partner_id = self.partner_id.id
            #sequence_code = 'register.payment.advance.supplier'

        return cuenta_deudora,cuenta_acreedora,partner_id

    def get_move_register(self):
        # se crea el asiento contable para el registro
        name = None

        cuenta_deudora, cuenta_acreedora,partner_id,sequence_code,is_supplier,is_customer = self.get_account_advance()
        #busca la secuencia del diario y se lo asigno a name
        if self.partner_id.es_cliente and not cuenta_acreedora and self.type_advance == False:
                raise exceptions.Warning(_('El cliente no tiene configurado la cuenta contable de anticipo'))
        elif self.partner_id.es_proveedor and not cuenta_deudora and self.type_advance:
                raise exceptions.Warning(_('El socio no tiene configurado la cuenta contable de anticipo'))

        else:
            name = self.env['ir.sequence'].with_context(ir_sequence_date=self.date_advance).next_by_code(sequence_code)
            vals = {
                # 'name': name,
                'date': self.date_advance,
                'line_ids': False,
                'state': 'draft',
                'journal_id': self.bank_account_id.id,
            }
            move_obj = self.env['account.move']
            move_id = move_obj.create(vals)
            #Si el pago es en moneda extranjera $
            if self.currency_id.name != self.env.company.currency_id.name:
                self.rate = currency_rate = self.amount_rate
                self.amount_currency_apply = self.currency_id.id
                if not currency_rate:
                    raise exceptions.Warning(_('Asegurese de tener la multimoneda configurada y registrar la tasa de la fecha del anticipo'))
                money = self.amount_advance
                move_advance_ = {
                    'account_id': cuenta_acreedora,
                    'company_id': self.partner_id.company_id.id,
                    'currency_id': self.currency_id.id,
                    'date_maturity': False,
                    'ref': self.ref,
                    'date': self.date_advance,
                    'partner_id': self.partner_id.id,
                    'move_id': move_id.id,
                    'name': name,
                    'credit':  self.amount_advance*currency_rate,
                    'debit': 0.0,
                    'amount_currency': -money,
                }
                asiento = move_advance_
                move_line_obj = self.env['account.move.line']
                move_line_id1 = move_line_obj.with_context(check_move_validity=False).create(asiento)
                asiento['amount_currency'] = money
                # asiento['currency_id'] = ""
                asiento['account_id'] = cuenta_deudora
                asiento['credit'] = 0.0
                asiento['debit'] = self.amount_advance*currency_rate
                move_line_id2 = move_line_obj.create(asiento)
                move_id.action_post()

                if move_line_id1 and move_line_id2:
                    # if self.partner_id.es_cliente == False:
                    # res = {'state': 'available', 'move_id': move_id.id, 'supplier':True, 'amount_available':self.amount_advance,'name':name}
                    # else:
                    # res = {'state': 'available', 'move_id': move_id.id, 'customer':True, 'amount_available':self.amount_advance,'name':name}

                    # return super(AccountAdvancePayment, self).write(res)

                    if self.partner_id.es_proveedor and self.type_advance:
                        res = {'state': 'available', 'move_id': move_id.id, 'supplier': True,
                               'amount_available': self.amount_advance, 'name': name, 'is_supplier': True,}
                    else:
                        res = {'state': 'available', 'move_id': move_id.id, 'customer': True,
                               'amount_available': self.amount_advance, 'name': name, 'is_customer': True,}

                    return super(AccountAdvancePayment, self).write(res)
            else:
                self.amount_currency_apply = self.currency_id.id
                move_advance_ = {
                    'account_id': cuenta_acreedora,
                    'company_id': self.partner_id.company_id.id,
                    'date_maturity': False,
                    'ref': self.ref,
                    'date': self.date_advance,
                    'partner_id': self.partner_id.id,
                    'move_id': move_id.id,
                    'name': name,
                    'credit': self.amount_advance,
                    'debit': 0.0,
                    'amount_currency': 0.0,
                }
                asiento = move_advance_
                move_line_obj = self.env['account.move.line']
                move_line_id1 = move_line_obj.with_context(check_move_validity=False).create(asiento)
                asiento['amount_currency'] = 0.0
                asiento['account_id'] = cuenta_deudora
                asiento['credit'] = 0.0
                asiento['debit'] = self.amount_advance

                move_line_id2 = move_line_obj.create(asiento)
                move_id.action_post()

                if move_line_id1 and move_line_id2:
                    #if self.partner_id.es_cliente == False:
                        #res = {'state': 'available', 'move_id': move_id.id, 'supplier':True, 'amount_available':self.amount_advance,'name':name}
                    #else:
                        #res = {'state': 'available', 'move_id': move_id.id, 'customer':True, 'amount_available':self.amount_advance,'name':name}

                    #return super(AccountAdvancePayment, self).write(res)

                    if self.partner_id.es_proveedor and self.type_advance:
                        res = {'state': 'available', 'move_id': move_id.id, 'supplier':True, 'amount_available':self.amount_advance,'name':name, 'is_supplier':True,}
                    else:
                        res = {'state': 'available', 'move_id': move_id.id, 'customer':True, 'amount_available':self.amount_advance,'name':name, 'is_customer':True,}

                    return super(AccountAdvancePayment, self).write(res)
        return True

    def get_move_apply(self):
        # se crea el asiento contable para el resgitro de la aplicacion del anticipo

        cuenta_deudora, cuenta_acreedora = self.get_account_apply()

        vals = {
            'date': self.date_apply,
            'line_ids': False,
            'state': 'draft',
            'journal_id': self.bank_account_id.id,
        }
        move_apply_obj = self.env['account.move']
        move_apply_id = move_apply_obj.create(vals)
        if self.amount_currency_apply == self.env.company.currency_id:
            money_base = round((self.amount_apply / self.amount_rate_apply), 2)
            money = self.amount_apply
        else:
            money_base = self.amount_apply
            money = round((self.amount_apply * self.amount_rate_apply), 2)
        move_advance_ = {
            'account_id': cuenta_acreedora,
            'company_id': self.env.company.id,
            'currency_id': self.amount_currency_apply.id,
            'date_maturity': False,
            'ref': self.ref,
            'date': self.date_apply,
            'partner_id': self.partner_id.id,
            'move_id': move_apply_id.id,
            'name': self.name,
            'credit': money,
            'debit': 0.0,
            'amount_currency': -money_base,
        }

        asiento_apply = move_advance_
        move_line_obj = self.env['account.move.line']
        move_line_obj.with_context(check_move_validity=False).create(asiento_apply)

        asiento_apply['amount_currency'] = money_base
        asiento_apply['account_id'] = cuenta_deudora
        asiento_apply['credit'] = 0.0
        asiento_apply['debit'] = money
        move_line_obj.create(asiento_apply)
        move_apply_id.action_post()
        self.move_apply_id = move_apply_id.id
        return True

    def action_refund_amount_available(self):
        # Crea un asiento contable con el monto residual disponible que queda de una aplicacion de anticipo
        if self.state == 'available':

            cuenta_deudora, cuenta_acreedora, partner_id = self.get_account_refund()

            vals = {
                # 'name': self.name,
                'date': self.date_apply,
                'line_ids': False,
                'state': 'draft',
            }
            move_obj = self.env['account.move']
            move_refund_id = move_obj.create(vals)
            if self.currency_id == self.env.company.currency_id:
                move_advance_ = {
                    'account_id': cuenta_acreedora,
                    'company_id': self.partner_id.company_id.id,
                    'date_maturity': False,
                    'ref': self.ref,
                    'date': self.date_apply,
                    'partner_id': self.partner_id.id,
                    'move_id': move_refund_id.id,
                    'name': self.name,
                    'credit': self.amount_available,
                    'debit': 0.0,
                }

                asiento = move_advance_
                move_line_obj = self.env['account.move.line']
                move_line_id1 = move_line_obj.with_context(check_move_validity=False).create(asiento)

                asiento['account_id'] = cuenta_deudora
                asiento['credit'] = 0.0
                asiento['debit'] = self.amount_available
            else:
                move_advance_ = {
                    'account_id': cuenta_acreedora,
                    'company_id': self.partner_id.company_id.id,
                    'currency_id': self.currency_id.id,
                    'date_maturity': False,
                    'ref': self.ref,
                    'date': self.date_apply,
                    'partner_id': self.partner_id.id,
                    'move_id': move_refund_id.id,
                    'name': self.name,
                    'credit': self.amount_available * self.amount_rate_apply,
                    'debit': 0.0,
                    'amount_currency': -(self.amount_available),
                }

                asiento = move_advance_
                move_line_obj = self.env['account.move.line']
                move_line_id1 = move_line_obj.with_context(check_move_validity=False).create(asiento)

                asiento['amount_currency'] = self.amount_available
                asiento['account_id'] = cuenta_deudora
                asiento['credit'] = 0.0
                asiento['debit'] = self.amount_available * self.amount_rate_apply

            move_line_id2 = move_line_obj.create(asiento)
            move_refund_id.action_post()

            if move_line_id1 and move_line_id2:
                res = {'state': 'cancel',
                       'move_refund_id': move_refund_id.id,
                       'amount_invoice':0,
                       'amount_apply':0,
                       'invoice_id':None}
                self.write(res)
            return True

    def action_cancel(self):
        # accion del boton cancelar para el resgitro cuando esta available o cancelar la aplicacion con esta es estado paid
        if self.state == 'available':
            if not self.move_apply_id:
                for advance in self:
                    for move in advance.move_id:
                        move_reverse = move._reverse_moves(cancel=True)
                        if len(move_reverse)==0:
                            raise UserError(_('No se reversaron los asientos asociados'))
                        res = {'state': 'cancel'}
                        return super(AccountAdvancePayment, self).write(res)
            else:
                raise exceptions.ValidationError('El anticipo ya tiene una aplicacion')

        elif self.state == 'paid':
            dominio = [('name', '=', self.name),
                       ('move_id','=',self.move_apply_id.id),
                       ('reconciled','=',True)]
            obj_move_line = self.env['account.move.line'].search(dominio)
            if obj_move_line:
                raise exceptions.ValidationError(('El anticipo ya tiene una aplicacion en la factura %s') % self.invoice_id.name)
            else:
                for advance in self:
                    for move in advance.move_apply_id:
                        move_reverse = move._reverse_moves(cancel=True)
                        if len(move_reverse)== 0:
                            raise UserError(_('No se reversaron los asientos asociados'))

                    dominio_new = [('name','=',self.name),('state','=','available')]
                    reg_new = self.search(dominio_new)

                    if reg_new:
                        result= super(AccountAdvancePayment,reg_new).write({'amount_available':self.amount_available + self.amount_apply})
                    else:
                        self.copy()

            res = {'state':'cancel'}
            return super(AccountAdvancePayment, self).write(res)
        return True

    def set_to_draft(self):
        # convierte a borrador el regsitro de anticipo
        res = {'state': 'draft'}
        return super(AccountAdvancePayment, self).write(res)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def assert_balanced(self):
        if not self.ids:
            return True
        mlo = self.env['account.move.line'].search([('move_id', '=',self.ids[0])])
        if not mlo.reconcile:
            super(AccountMove, self).assert_balanced(fields)
        return True

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency = fields.Many2one('res.currency', string='BS currency',
                                       default=lambda self: self.env.company.currency_id)
