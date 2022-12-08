# -*- coding: utf-8 -*-
{
    'name': "pleni_user_order",
    'author': "Oriana Graterol",
    'website': "https://www.pleni.app",
    'category': 'Inventory',
    'version': '0.1',
    'depends': ['base', 'website', 'website_sale', 'portal', 'payment', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}