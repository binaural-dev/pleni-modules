{
    "name": "Gestión de retenciones leyes venezolanas",
    "version": "1.0",
    "author": "Localizacion Venezolana",
    "category": 'Contabilidad',
    "depends": ['account', 'base_vat', 'account_accountant', 'base', '3mit_account_fiscal_requirements','3mit_grupo_localizacion', '3mit_rates'],
    'data': [
        'view/base_withholding_view.xml',
        'view/account_journal_view.xml',
    ],
    'installable': True,
    'active': True,
}
