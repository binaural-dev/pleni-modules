from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    salesman_id = fields.Many2one(
        'res.salesman', string='Vendedor')

    @api.onchange('partner_id')
    def _set_salesman(self):
        for record in self:
            partner = self.env['res.partner'].search(
                [('id', '=', record.partner_id.id)])
            record.salesman_id = partner.salesman_id

    @api.model_create_multi
    def create(self, vals_list):
        for element in vals_list:
            if 'partner_id' in vals_list:
                partner = self.env['res.partner'].search(
                    [('name', '=', element['partner_id'])]
                )
                element['salesman_id'] = partner.salesman_id
        res = super(SaleOrderInherit, self).create(vals_list)
        return res
