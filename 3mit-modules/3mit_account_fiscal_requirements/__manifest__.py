# coding: utf-8

{
    'name': 'Requerimientos Fiscales Venezuela',
    'version': '1.2',
    'category': 'Accounting',
    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'summary': """
        Requerimientos fiscales exigidos por las leyes venezolanas.""",
    'description': """
        Agrega los requerimientos fiscales exigidos por las leyes venezolanas.\n
        Colaborador: Maria Carreño, Kleiver Pérez.""",

    'depends': [
        'account',
        'base_vat',
        'account_accountant',
        '3mit_grupo_localizacion',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/l10n_ut_data.xml',
        'wizard/search_info_partner_seniat.xml',
        'wizard/wizard_nro_ctrl_view.xml',
        'view/res_company_view.xml',
        'view/l10n_ut_view.xml',
        'view/account_tax_view.xml',
        'view/account_invoice_view.xml',
        'view/nro_ctrl_secuencial_customer.xml',
    ],
    'installable': True,
}
