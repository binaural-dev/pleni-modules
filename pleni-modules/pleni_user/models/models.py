# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class requiredFieldsResPartner(models.Model):
    _inherit = 'res.partner'

    document_type = fields.Selection([('V', 'V'), ('E', 'E'), ('P', 'P')])
    identification_document = fields.Char()
    rif_type = fields.Selection(
        [('J', 'J'), ('G', 'G'), ('E', 'E'), ('V', 'V')])
    identification_rif = fields.Char()

    def xor(self, tipo, numero):
        return bool((tipo and not numero) or (not tipo and numero) or (tipo and numero))

    def rif_len(self, len):
        if len < 9 or len > 9:
            raise UserError('El RIF debe contener 9 numeros')

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            res = super(requiredFieldsResPartner, self).create(vals_list)
        return res

    def write(self, vals):
        for element in self:
            res = super(requiredFieldsResPartner, self).write(vals)
        return res

    @api.constrains('vat', 'country_id')
    def check_vat(self):
        # The context key 'no_vat_validation' allows you to store/set a VAT number without doing validations.
        # This is for API pushes from external platforms where you have no control over VAT numbers.
        if self.env.context.get('no_vat_validation'):
            return
        partners_with_vat = self.filtered('vat')

    def get_count_wish_products(self):
        count = self.env['product.wishlist'].search([('partner_id', '=', self.id), ('write_date', '>', '2022-12-31 00:00:00')])
        return True if len(count) == 0 else False
