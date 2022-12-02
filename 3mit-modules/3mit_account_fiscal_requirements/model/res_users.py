# coding: utf-8

from odoo import models, api, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals):
        """To create a new record,
        adds a Boolean field to true
        indicates that the partner is a company
        """
        if self._context is None:
            context = {}
        context = dict(self._context or {})
        context.update({'create_company': True})
        self.with_context(context)
        return super(ResUsers, self).create(vals)

    def write(self, values):
        """ To write a new record,
        adds a Boolean field to true
        indicates that the partner is a company
        """
        context = dict(self._context or {})
        context.update({'create_company': True})
        self.with_context(context)
        return super(ResUsers, self).write(values)

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    make_visible = fields.Boolean(string="User", compute='get_user')

    @api.depends('make_visible')
    def get_user(self, ):
        user_crnt = self._uid
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('3mit_grupo_localizacion.group_localizacion'):
            self.make_visible = True
        else:
            self.make_visible = False

