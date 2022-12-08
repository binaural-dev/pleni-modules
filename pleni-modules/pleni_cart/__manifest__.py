# -*- coding: utf-8 -*-
{
    'name': "pleni_cart",
    'author': "Oriana Graterol",
    'website': "https://www.pleni.app",
    'category': 'Website/Ecommerce',
    'version': '0.1',
    'depends': [
        'atharva_theme_base',
        'base',
        'product',
        'delivery',
        'website_sale', 
        'website_uom_select_suggetion_spt', 
        'website_sale_delivery', 
        'website',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/assets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
