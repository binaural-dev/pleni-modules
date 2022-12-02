# -*- coding: utf-8 -*-
{
    'name': 'Account Advanced Payment',

    'summary': 'Registro de Anticipo para proveedores y clientes.',

    'description': '''
Registro de Anticipos para ser aplicados a las facturas de clientes y proveedores,
asi como los reversos de los mismos.
============================
Colaborador: Maria Carreno
''',
    'author': '3MIT',
    'website': "https://www.3mit.dev/",
    'version': '1.1.3',
    'category': 'Accounting',
    # Depends,  es una lista donde se agregan los módulos que deberían estar instalados (Módulos dependencia) para que el modulo pueda ser instalado en Odoo.
    'depends': ['base', 'web', 'mail', 'account', '3mit_grupo_localizacion', '3mit_account_fiscal_requirements', '3mit_rates'],
    # Data, es una lista donde se agregan todas las vistas del módulo, es decir los archivos.xml y archivos.csv.
    'data': [
            'security/ir.model.access.csv',
            'view/account_advance_payment.xml',
            'data/sequence_advance_data.xml',
            'view/res_partner_view.xml',
            'view/invoice_view.xml',
            'view/res_company_views.xml',
            'security/group.xml',
            'view/account_journal_view.xml',
        ],
    'installable': True,
    'active': True,
}
