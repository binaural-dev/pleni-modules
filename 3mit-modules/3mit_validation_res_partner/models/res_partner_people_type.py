# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('company_type')
    def change_country_id_partner(self):
        if self.company_type and self.company_type == 'person':
            self.country_id = 238
        elif self.company_type == 'company':
            self.country_id = False

    people_type_individual = fields.Selection([
        ('pnre', 'PNRE Persona Natural Residente'),
        ('pnnr', 'PNNR Persona Natural No Residente')
        ], string='Tipo de Persona individual')
    people_type_company = fields.Selection([
        ('pjdo', 'PJDO Persona Jurídica Domiciliada'),
        ('pjnd', 'PJND Persona Jurídica No Domiciliada')], string='Tipo de Persona compañía')
