# -*- coding: utf-8 -*-
{
    'name': "pleni_wishlist",
    'author': "Oriana Graterol",
    'website': "https://www.pleni.app",
    'category': 'Website/Products',
    'version': '0.1',
    'depends': [
        'base',
        'website_sale',
        'website',
        'website_sale_wishlist',
        'product',
        'theme_laze',
        'binaural_sitio_web'
    ],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        "views/assets.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}