# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompanyConfig(models.Model):
    _inherit = 'res.company'

    def _get_country(self):
        country = self.env['res.country'].search([('id', '=', '238')], limit=1)
        if country.id:
            return country.id

    # campos para el diario de anticipos para la aplicacion de los anticipos y las cuentas de compra y ventas
    advance_journal_id = fields.Many2one('account.journal', 'Diario de Anticipos', company_dependent=True)
    advance_account_purchase_id = fields.Many2one('account.account', 'Cuenta de Anticipos de Compras')
    advance_account_sale_id = fields.Many2one('account.account', 'Cuenta de Anticipos de ventas')

    # campos para ocultar la localizacion venezolana segun la compañia
    loc_ven = fields.Boolean('Localizacion VEN', compute="_compute_loc_ven", store=True)
    country_id = fields.Many2one('res.country', string="Country", default=_get_country, required=True)

    @api.depends('country_id')
    def _compute_loc_ven(self):
        for company in self:
            if company.country_id.code == 'VE':
                company.loc_ven = True
            else:
                company.loc_ven = False
            if not isinstance(company.id, models.NewId):
                if company.loc_ven == True :
                    menus = self.env["ir.ui.menu"].search([])
                    for menu in menus:
                        if menu.name.find('(VE)') != -1:
                            menu.company_ids = [(4, company.id)]
                else:
                    menus = self.env["ir.ui.menu"].search([])
                    for menu in menus:
                        if menu.name.find('(VE)') != -1 and menu.company_ids:
                            menu.company_ids = [(3, company.id)]


    
