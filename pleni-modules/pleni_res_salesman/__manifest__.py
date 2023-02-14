# -*- coding: utf-8 -*-
{
    'name': "Pleni - Resource Salesman",
    'version': '0.1.6',
    'category': 'Uncategorized',
    'license': 'GPL-3',
    'author': "Manuel Escalante",
    'website': "https://pleni.app",
    'depends': ['base', 'sale', 'binaural_contactos_configuraciones'],
    'data': [
        'security/ir.model.access.csv',
        'security/salesman_security.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/res_salesman_view.xml',
    ]
}
