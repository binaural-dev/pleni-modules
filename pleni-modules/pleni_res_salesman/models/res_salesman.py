from odoo import models, fields, api
from datetime import datetime


class Salesman(models.Model):
    _name = 'res.salesman'
    _description = 'Model to save salesman information.'

    SALESMAN_ROLE = [
        ('hunter', 'Hunter'),
        ('farmer', 'Farmer'),
        ('keyAccount', 'Key Account Manager'),
        ('inboundSales', 'Inbound Sales'),
        ('doNotUse', 'Do Not Use')
    ]

    name = fields.Char(string='Nombre', required=True)
    saleman_role = fields.Selection(
        SALESMAN_ROLE, string='Rol del vendedor', required=True)
    email = fields.Char(string='Email',)
    state_id = fields.Many2one(
        'res.country.state', string='Estado', required=True, domain="[('country_id', '=', 238), ('is_active', '=', True)]")  # Domain filter with ID 238 (Venezuela)
    zone = fields.Char(string='Zona')
    admission_date = fields.Date(
        string='Fecha de unión', default=datetime.today(), required=True)
    active = fields.Boolean(default=True)
    deactivation_date = fields.Date(
        string='Fecha de desactivación', store=True, compute='_compute_active')
    sale_order_ids = fields.One2many(
        'sale.order', 'salesman_id', string='Ordenes de venta', readonly=True)
    res_partner_ids = fields.One2many(
        'res.partner', 'salesman_id', string='Clientes', readonly=True)

    @api.depends('active')
    def _compute_active(self):
        for record in self:
            if record.active == False:
                record.deactivation_date = datetime.today()
            else:
                record.deactivation_date = None
