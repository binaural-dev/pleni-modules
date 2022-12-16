# -*- coding: utf-8 -*-
{
    'name': "Retención de IVA",

    'summary': """
        Modulo que automatiza los procesos de retención de IVA según las leyes de Venezuela""",

    'description': """
        Esta versión fue adecuada para la localización view. Retención de porcentaje en facturas de proveedor automáticas, con uso de impuesto de 75% o 100% según sea la necesidad. También se realizó un pequeño cambio para que al cancelar la retención autómaticamente se destilde el campo de factura retenida. 
    """,

    'author': "Christian Isturiz",
    'website': "https://3mit.dev/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base_vat','base','account','3mit_base_withholdings','web','3mit_grupo_localizacion', 'account_debit_note', '3mit_account_fiscal_requirements'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'wizard/wizard_retention_view.xml',
        'wizard/record_retention_view.xml',
        'wizard/record_retention_suppliers.xml',
        'wizard/record_group_retention.xml',
        'view/generate_txt_view.xml',
        'view/account_invoice_view.xml',
        'view/account_view.xml',
        'view/partner_view.xml',
        'view/wh_iva_view.xml',
        'view/retention_group_view.xml',
        'report/withholding_group_vat_report.xml',
        'view/account_move_reversal_inherit.xml',
        'security/group.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
