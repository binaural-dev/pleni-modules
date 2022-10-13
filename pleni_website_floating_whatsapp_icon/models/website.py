from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    atc_mobile_number = fields.Char(string="Número de teléfono (Whatsapp)")
