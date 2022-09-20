# coding: utf-8
from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals):
        if vals:
            if vals[0].get('invoice_origin'):
                purchase_order = self.env['purchase.order'].search([('name', '=', vals[0].get('invoice_origin')), ('company_id', '=', vals[0].get('company_id'))])
                if purchase_order:
                    vals[0].update({'partner_id': purchase_order.partner_id.id})

            if vals[0].get('partner_id') and self.loc_ven:
                partner_id = vals[0].get('partner_id')
                partner_obj = self.env['res.partner'].search([('id', '=', partner_id)])
                if partner_obj.company_type == 'person' and not partner_obj.identification_id:
                    raise UserError("Advertencia! \nEl Proveedor no posee Documento Fiscal. Por favor diríjase a la configuación de %s, y realice el registro correctamente para poder continuar" % (partner_obj.name))
                if partner_obj.company_type == 'company':
                    if partner_obj.people_type_company == 'pjdo' and not partner_obj.rif:
                        raise UserError("Advertencia! \nEl Proveedor no posee Documento Fiscal. Por favor diríjase a la configuación de %s, y realice el registro correctamente para poder continuar" % (partner_obj.name))

        for element in vals:
            if element.get("invoice_line_ids", False) and element.get("line_ids", False):
                for line in element["invoice_line_ids"]:
                    for line2 in element["line_ids"]:
                        if line[1] == line2[1]:
                            if line[2] != False and line2[2] != False:
                                if line[2].get("concept_id", False):
                                    line2[2]["concept_id"] = line[2]["concept_id"]

        res = super(AccountMoveInherit, self).create(vals)
        return res

    def write(self, vals):
        for move_account in self:
            if move_account.move_type == 'in_invoice' and move_account.invoice_origin:
                order_purchase = self.env['purchase.order'].search([('name', '=', self.invoice_origin), ('company_id', '=', self.company_id.id)])
                if order_purchase:
                    vals.update({'partner_id': order_purchase.partner_id.id})
        if vals.get('partner_id') and self.loc_ven:
            partner_id = vals.get('partner_id')
            partner_obj = self.env['res.partner'].search([('id', '=', partner_id)])
            if partner_obj.company_type == 'person' and not partner_obj.identification_id:
                raise UserError("Advertencia! \nEl Proveedor no posee Documento Fiscal. Por favor diríjase a la configuación de %s, y realice el registro correctamente para poder continuar" % (partner_obj.name))
            if partner_obj.company_type == 'company':
                if partner_obj.people_type_company == 'pjdo' and not partner_obj.rif:
                    raise UserError("Advertencia! \nEl Proveedor no posee Documento Fiscal. Por favor diríjase a la configuación de %s, y realice el registro correctamente para poder continuar" % (partner_obj.name))

        # Actualizacion del concepto
        if vals.get("invoice_line_ids", False) and vals.get("line_ids", False):
            for line in vals["invoice_line_ids"]:
                for line2 in vals["line_ids"]:
                    if line[1] == line2[1]:
                        if len(line) > 2 and len(line2) > 2:
                            if line[2] != False:
                                if line[2].get("concept_id", False):
                                    if line2[2] != False:
                                        line2[2]["concept_id"] = line[2]["concept_id"]
                                    else:
                                        line2[0] = line[0]
                                        line2[2] = line[2]

        res = super(AccountMoveInherit, self).write(vals)
        return res

    @api.onchange('partner_id')
    def _compute_partner(self):
        # self.people_type = self.partner_id.people_type_company
        self.customer_rank1 = self.partner_id.customer_rank
        self.supplier_rank1 = self.partner_id.supplier_rank
        self.people_type_company1 = self.partner_id.people_type_company
        self.people_type_individual1 = self.partner_id.people_type_individual
        self.company_type1 = self.partner_id.company_type
        return

    # Campos proveedores
    nro_planilla_impor = fields.Char(string='Nro de Planilla de Importacion')
    nro_expediente_impor = fields.Char(string='Nro de Expediente de Importacion')
    fecha_importacion = fields.Date(string='Fecha de la planilla de Importación')
    supplier_rank1 = fields.Integer(related='partner_id.supplier_rank')
    # Campos clientes
    customer_rank1 = fields.Integer(related='partner_id.customer_rank')
    # Campos para ambos
    partner_id = fields.Many2one('res.partner', readonly=True,
                                 domain="['|',('customer_rank', '>=', 0),('supplier_rank', '>=', 0)]",
                                 string='Partner')
    rif = fields.Char(string="RIF", related='partner_id.rif', store=True, states={'draft': [('readonly', True)]})
    identification_id1 = fields.Char(string='Documento de Identidad', related='partner_id.identification_id',
                                     store=True, states={'draft': [('readonly', True)]})
    nationality1 = fields.Selection([('V', 'Venezolano'), ('E', 'Extranjero'), ('P', 'Pasaporte')],
                                    string="Tipo Documento", related='partner_id.nationality', store=True,
                                    states={'draft': [('readonly', True)]})
    people_type_company1 = fields.Selection([('pjdo', 'PJDO Persona Jurídica Domiciliada'),
                                             ('pjnd', 'PJND Persona Jurídica No Domiciliada')],
                                            string='Tipo de Persona compañía val')
    people_type_individual1 = fields.Selection([('pnre', 'PNRE Persona Natural Residente'),
                                                ('pnnr', 'PNNR Persona Natural No Residente')],
                                               string='Tipo de Persona individual val')
    company_type1 = fields.Selection(string='Company Type',
                                     selection=[('person', 'Individual'), ('company', 'Company')])
    create_invoice = fields.Boolean(string='Crear factura', default=False)


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    people_type_company1 = fields.Selection([('pjdo', 'PJDO Persona Jurídica Domiciliada'),
                                             ('pjnd', 'PJND Persona Jurídica No Domiciliada')],
                                            string='Tipo de Persona compañía val')
    people_type_individual1 = fields.Selection([('pnre', 'PNRE Persona Natural Residente'),
                                                ('pnnr', 'PNNR Persona Natural No Residente')],
                                               string='Tipo de Persona individual val')
    company_type1 = fields.Selection(string='Company Type',
                                     selection=[('person', 'Individual'), ('company', 'Company')])
    create_invoice = fields.Boolean(string='Crear factura', default=False)
