from odoo import models, fields


class CustomSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_send_sms = fields.Boolean(
        string="Mensaje Directo de Whatsapp",
        implied_group='pleni_whatsapp_integration.group_send_sms'
    )
