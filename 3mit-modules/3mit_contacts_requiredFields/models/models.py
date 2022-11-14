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
            if 'document_type' in element:
                if element['document_type'] == 'V':
                    element['nationality'] = 'V'
                    if 'identification_document' in element:
                        element['identification_id'] = element['identification_document']
                elif element['document_type'] == 'E':
                    element['nationality'] = 'E'
                    if 'identification_document' in element:
                        element['identification_id'] = element['identification_document']
                elif element['document_type'] == 'P':
                    element['nationality'] = 'P'
                    if 'identification_document' in element:
                        element['identification_id'] = element['identification_document']
            if 'rif_type' in element or self.rif_type:
                rif_type = element['rif_type'] if 'rif_type' in element else self.rif_type
                if rif_type == False:
                    rif_type = ""
            if 'identification_rif' in element or self.identification_rif:
                identification_rif = element['identification_rif'] if 'identification_rif' in element else self.identification_rif
                if identification_rif == False:
                    identification_rif = ""
                if identification_rif:
                    self.rif_len(len(identification_rif))
                if self.xor(rif_type, identification_rif) == True:
                    element['rif'] = rif_type + '-' + identification_rif
        res = super(requiredFieldsResPartner, self).create(vals_list)
        return res

    def write(self, vals):
        for element in self:
            if 'document_type' in vals or element.document_type:
                document_type = vals['document_type'] if 'document_type' in vals else element.document_type
                if document_type == 'V':
                    if 'nationality' in vals:
                        vals['nationality'] = 'V'
                    if 'identification_document' in vals:
                        if vals['identification_document']:
                            vals['identification_id'] = vals['identification_document']
                elif document_type == 'E':
                    if 'nationality' in vals:
                        vals['nationality'] = 'E'
                    if 'identification_document' in vals:
                        if vals['identification_document']:
                            vals['identification_id'] = vals['identification_document']
                elif document_type == 'P':
                    if 'nationality' in vals:
                        vals['nationality'] = 'P'
                    if 'identification_document' in vals:
                        if vals['identification_document']:
                            vals['identification_id'] = vals['identification_document']
            if 'rif_type' in vals or element.rif_type or element.rif_type == False:
                rif_type = vals['rif_type'] if 'rif_type' in vals else element.rif_type
                if rif_type == False:
                    rif_type = ""
            if 'identification_rif' in vals or element.identification_rif or element.identification_rif == False:
                identification_rif = vals['identification_rif'] if 'identification_rif' in vals else element.identification_rif
                if identification_rif == False:
                    identification_rif = ""
                if identification_rif:
                    element.rif_len(len(identification_rif))
                if element.xor(rif_type, identification_rif) == True:
                    vals['rif'] = rif_type + '-' + identification_rif
        res = super(requiredFieldsResPartner, self).write(vals)
        return res
