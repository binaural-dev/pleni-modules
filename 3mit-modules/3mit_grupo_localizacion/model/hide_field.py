from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven

class SaleOrderHide(models.Model):
    _inherit = 'sale.order'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven


class SaleOrderLineHide(models.Model):
    _inherit = 'sale.order.line'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven


class AccountMoveLineHide(models.Model):
    _inherit = 'account.move.line'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven


class ResPartnerHide(models.Model):
    _inherit = 'res.partner'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven


class ProductTemplateHide(models.Model):
    _inherit = 'product.template'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven

class PurchaseOrderHide(models.Model):
    _inherit = 'purchase.order'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven


class AccountMoveHide(models.Model):
    _inherit = 'account.move'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven


class AccountTaxHide(models.Model):
    _inherit = 'account.tax'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven

class rates(models.Model):
    _inherit = 'res.currency.rate'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven

class redirectToRates(models.Model):
    _inherit = 'res.currency'

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven

class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    loc_ven = fields.Boolean(compute='_change_status', default=lambda self: self.env.company.loc_ven)

    def _change_status(self):
        self.loc_ven = self.env.company.loc_ven