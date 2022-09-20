# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompanyConfig(models.Model):
    _inherit = 'res.company'
    # Se crea un campo para el diario de anticipos para la aplicacion de los anticipos y las cuentas de compra y ventas

    advance_journal_id = fields.Many2one('account.journal', 'Diario de Anticipos', company_dependent=True, groups="3mit_grupo_localizacion.group_localizacion")
    advance_account_purchase_id = fields.Many2one('account.account', 'Cuenta de Anticipos de Compras', groups="3mit_grupo_localizacion.group_localizacion")
    advance_account_sale_id = fields.Many2one('account.account', 'Cuenta de Anticipos de ventas', groups="3mit_grupo_localizacion.group_localizacion")
    loc_ven = fields.Boolean('Localizacion VEN')



    
