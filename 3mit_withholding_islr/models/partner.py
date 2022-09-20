# coding: utf-8
##############################################################################
from odoo import api
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'


    islr_withholding_agent = fields.Boolean(
            '¿Agente de retención de ingresos?', default=True, groups="3mit_grupo_localizacion.group_localizacion",
            help="Verifique si el partner es un agente de retención de ingresos")
    spn = fields.Boolean(
            '¿Es una sociedad de personas físicas?', groups="3mit_grupo_localizacion.group_localizacion",
            help='Indica si se refiere a una sociedad de personas físicas.')
    islr_exempt = fields.Boolean(
            '¿Está exento de retención de ingresos?', groups="3mit_grupo_localizacion.group_localizacion",
            help='Si el individuo está exento de retención de ingresos')
    purchase_islr_journal_id = fields.Many2one('account.journal', 'Diario de Compra para ISLR', company_dependent=True, groups="3mit_grupo_localizacion.group_localizacion",)
    sale_islr_journal_id = fields.Many2one('account.journal', 'Diario de Venta para ISLR', company_dependent=True, groups="3mit_grupo_localizacion.group_localizacion",)
    tax_islr = fields.Many2one('account.tax', 'Impuesto ISLR Compras', domain=[('type_tax', '=', "islr_ret")], company_dependent=True, groups="3mit_grupo_localizacion.group_localizacion",)

    def copy(self, default=None):
        """ Initialized id by duplicating
        """
        # NOTE: use ids argument instead of id for fix the pylint error W0622.
        # Redefining built-in 'id'
        if default is None:
            default = {}
        default = default.copy()
        default.update({
            'islr_withholding_agent': 1,
            'spn': 0,
            'islr_exempt': 0,
            'rif': False,
            'identification_id': False,

        })

        return super(ResPartner, self).copy(default)
