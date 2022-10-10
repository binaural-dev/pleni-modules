from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    hunter_id = fields.Many2one('res.salesman', string='Hunter',
                                domain="[('saleman_role', '=', 'hunter'), ('active', '=', True)]")
    salesman_id = fields.Many2one('res.salesman', string='Farmer', required=True,
                                  domain="[('saleman_role', '=', 'farmer'), ('active', '=', True)]")

    @api.onchange('salesman_id')
    def _change_hunter(self):
        sales = self.env['sale.order'].search(
            [('partner_id', '=', self._origin.id)])
        if len(sales) == 0:
            self.hunter_id = self.salesman_id
