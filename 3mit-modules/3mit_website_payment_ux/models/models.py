# -*- coding: utf-8 -*-

from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortalInherit(CustomerPortal):
    def _prepare_orders_domain(self, partner):
        res = super(CustomerPortalInherit, self)._prepare_orders_domain(partner)
        return [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sale', 'done', 'sent', 'cancel'])
        ]
