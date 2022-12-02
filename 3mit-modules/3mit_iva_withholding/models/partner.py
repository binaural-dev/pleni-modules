# -*- coding: utf-8 -*-
# import logging
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    wh_iva_agent = fields.Boolean('¿Es Agente de Retención (IVA)?',
                                  help="Indique si el socio es un agente de retención de IVA", company_dependent=True)
    wh_iva_rate = fields.Float(
        string='Retención Ventas',
        help="Se coloca el porcentaje de la Tasa de retención de IVA")

    purchase_sales_id = fields.Many2one('account.journal', 'Diario de Venta para IVA', company_dependent=True)

    tax_percentage = fields.Many2one('account.tax', 'Retención Compras', company_dependent=True,
                                     domain="[('type_tax', '=', 'iva_ret')]")