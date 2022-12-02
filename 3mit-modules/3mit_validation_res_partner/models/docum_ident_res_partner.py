# -*- coding: UTF-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class ValidationDocument(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, values):
        for val in values:
            if val.get('company_id'):
                company = self.env['res.company'].search([('id', '=', val['company_id'])])
                if company.loc_ven == True:
                    if val.get('identification_id') and val.get('nationality'):
                        valor = val.get('identification_id')
                        nationality = val.get('nationality')
                        self.validation_document_ident(valor, nationality)
                    if val.get('identification_id'):
                        if not self.validate_ci_duplicate(val.get('identification_id', False), True):
                            raise UserError('El cliente o proveedor ya se encuentra registrado con el Documento: %s'
                                            % (val.get('identification_id', False)))
        return super(ValidationDocument, self).create(values)

    def write(self, vals):
        for s in self:
            if s.loc_ven:
                if vals.get('identification_id') and not vals.get('nationality'):
                    valor = vals.get('identification_id')
                    nationality = s.nationality
                    s.validation_document_ident(valor, nationality)
                if vals.get('identification_id') and vals.get('nationality'):
                    valor = vals.get('identification_id')
                    nationality = vals.get('nationality')
                    s.validation_document_ident(valor, nationality)
                if vals.get('nationality') and not vals.get('identification_id'):
                    valor = s.identification_id
                    nationality = vals.get('nationality')
                    s.validation_document_ident(valor, nationality)
                if not s.validate_ci_duplicate(vals.get('identification_id', False)):
                    raise UserError('El cliente o proveedor ya se encuentra registrado con el Documento: %s'
                                    % (vals.get('identification_id', False)))

                if vals.get('identification_id') and vals.get('nationality'):
                    vals['identification_id'] = vals.get('nationality')+'-'+vals.get('identification_id')
            res = super(ValidationDocument, s).write(vals)
            return res

    nationality = fields.Selection([
        ('V', 'Venezolano'),
        ('E', 'Extranjero'),
        ('P', 'Pasaporte')], string="Tipo Documento")
    identification_id = fields.Char(string='Documento de Identidad')
    value_parent = fields.Boolean(string='Valor parent_id', compute='compute_value_parent_id')

    @api.depends('company_type')
    def compute_value_parent_id(self):
        for rec in self:
            rec.value_parent = rec.parent_id.active

    @staticmethod
    def validation_document_ident(valor, nationality):
        return
        # if valor:
        #     if nationality == 'V' or nationality == 'E':
        #         if len(valor) == 7 or len(valor) == 8:
        #             if not valor.isdigit():
        #                 raise UserError('La Cédula solo debe ser Numerico. Por favor corregir para proceder a Crear/Editar el registro')
        #             return
        #         else:
        #             raise UserError('La Cedula de Identidad no puede ser menor que 7 cifras ni mayor a 8.')
        #     if nationality == 'P':
        #         if(len(valor) > 20) or (len(valor) < 10):
        #             raise UserError('El Pasaporte no puede ser menor que 10 cifras ni mayor a 20.')
        #         return

    def validate_ci_duplicate(self, valor, create=False):
        found = True
        partner_2 = self.search([('identification_id', '=', valor)])
        for cus_supp in partner_2:
            if create:
                if cus_supp and (cus_supp.customer_rank or cus_supp.supplier_rank):
                    found = False
                elif cus_supp and (cus_supp.customer_rank or cus_supp.supplier_rank):
                    found = False
        return found
