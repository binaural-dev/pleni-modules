# -*- coding: utf-8 -*-
{
    'name': "Pleni - Custom Fields",
    'version': '0.3',
    'category': 'Uncategorized',
    'license': 'GPL-3',
    'author': "Manuel Escalante",
    'website': "https://pleni.app",
    'depends': [
        'base',
        'account',
        'account_payment',
        'stock',
        'sale',
        'sale_stock',
        'product',
        'binaural_contactos_configuraciones'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/find_us_data.xml',
        'views/account_payment_view.xml',
        'views/find_us_view.xml',
        'views/res_partner_view.xml',
        'views/urbanization_area_view.xml',
        'views/view.xml',
        'views/menu_view.xml',
        'views/sale_order_view.xml',
        'views/sale_report_view.xml',
        'views/purchase_sale_supplier_client.xml'
    ]
}
