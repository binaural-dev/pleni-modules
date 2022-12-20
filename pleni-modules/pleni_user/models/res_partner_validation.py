# -*- coding: UTF-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import re


class ResPartnerRif(models.Model):
    _inherit = 'res.partner'

    rif = fields.Char(string='RIF')

    @api.model_create_multi
    def create(self, values):

        for val in values:
            if val.get("name") and not val.get("commercial_name"):
                val["commercial_name"] = val.get("name")
            # if val.get('rif'):
            #     if not self.validate_rif_er(val.get('rif')):
            #         raise UserError('El rif tiene el formato incorrecto. Ej: V-012345679, E-012345678, J-012345678 o G-012345678. Por favor verifique el formato y si posee los 9 digitos como se indica en el Ej. e intente de nuevo')
            #     if self.validate_rif_duplicate(val.get('rif')):
            #         raise UserError('El cliente o proveedor ya se encuentra registrado con el rif: %s y se encuentra activo'
            #                         % (val.get('rif')))
            if val.get('email'):
                if not self.validate_email_addrs(val.get('email'), 'email'):
                    raise UserError('El email es incorrecto. Ej: cuenta@dominio.xxx. Por favor intente de nuevo')
        return super(ResPartnerRif, self).create(values)

    def write(self, values):
        for s in self:
            # if s.loc_ven:
            #     if values:
            #         # if values.get("rif"):
            #         #     if not s.validate_rif_er(values.get("rif")):
            #         #         raise UserError(
            #         #             'El rif tiene el formato incorrecto. Ej: V-012345677, E-012345678, J-012345678 o G-012345678. Por favor verifique el formato y si posee los 9 digitos como se indica en el Ej. e intente de nuevo')
            #         #     if s.validate_rif_duplicate(values.get("rif")):
            #         #         raise UserError(
            #         #             'El cliente o proveedor ya se encuentra registrado con el rif: %s y se encuentra activo'
            #         #             % values.get("rif"))
            #         if values.get("email"):
            #             if not s.validate_email_addrs(values.get("email"), 'email'):
            #                 raise UserError('El email es incorrecto. Ej: cuenta@dominio.xxx. Por favor intente de nuevo')
            #         if values.get("name") and not s.commercial_name:
            #             values["commercial_name"] = values.get("name")
            return super(ResPartnerRif, s).write(values)
    
    @staticmethod
    def validate_rif_er(field_value):
        res = {}
        rif_obj = re.compile(r"^[V|E|J|G]+[-][\d]{5,9}", re.X)
        if rif_obj.search(field_value.upper()):
            if len(field_value) == 11:
                res = {
                    'rif': field_value
                }
            else:
                res = {}
        return res

    def validate_rif_duplicate(self, valor):
        if self.id:
            partner = self.env['res.partner'].search([('rif', '=', valor), ('id', '!=', self.id)])
        else:
            partner = self.env['res.partner'].search([('rif', '=', valor)])
        if partner:
            return True
        else:
            return False

    @staticmethod
    def validate_email_addrs(email, field):
        res = {}
        mail_obj = re.compile(r"""
                \b             # comienzo de delimitador de palabra
                [\w.%+-]       # usuario: Cualquier caracter alfanumerico mas los signos (.%+-)
                +@             # seguido de @
                [\w.-]         # dominio: Cualquier caracter alfanumerico mas los signos (.-)
                +\.            # seguido de .
                [a-zA-Z]{2,3}  # dominio de alto nivel: 2 a 6 letras en minúsculas o mayúsculas.
                \b             # fin de delimitador de palabra
                """, re.X)     # bandera de compilacion X: habilita la modo verborrágico, el cual permite organizar
        # el patrón de búsqueda de una forma que sea más sencilla de entender y leer.
        if mail_obj.search(email):
            res = {
                field: email
            }
        return res