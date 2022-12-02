# coding: utf-8
##############################################################################

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    automatic_income_wh= fields.Boolean(
            'Retención Automática', default=False,
            help='Cuando sea cierto, la retención de ingresos del proveedor se'
                 'validara automáticamente')