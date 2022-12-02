# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError


class AccountWhIvaInherit(models.Model):
    _inherit = 'wh.iva.group'

    res_partner_email = fields.Char(string="Email de la compañía", related="partner_id.email", required=True)
    user_id = fields.Many2one('res.users', 'Responsable', default=lambda self: self.env.user)

    def action_confirm(self):
        res = super(AccountWhIvaInherit, self).action_confirm()
        if self.res_partner_email:
            self.state = 'done'
            email_template_id = self.env.ref('3mit_email_iva_islr.ret_iva_template').id
            template = self.env['mail.template'].browse(email_template_id)

            empresa = None
            if self.partner_id.company_type == "company":
                empresa = self.partner_id
            elif self.partner_id.parent_id:
                empresa = self.partner_id.parent_id

            if empresa != None:
                if len(self.partner_id.child_ids) > 0:
                    emails_company = ""
                    for contact in self.partner_id.child_ids:
                        if contact.email:
                            emails_company = emails_company + contact.email + ";"

                    template.email_cc = emails_company

            template.send_mail(self.id, force_send=True)
            return res
        else:
            raise UserError('La compañía no tiene email asociado. Por favor, añada uno para continuar')

