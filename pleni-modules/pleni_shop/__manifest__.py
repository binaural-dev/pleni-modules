# -*- coding: utf-8 -*-
{
    'name': "pleni_shop",
    'author': "Oriana Graterol",
    'website': "https://www.pleni.app",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'website_sale', 'sale', 'web', 'website_uom_select_suggetion_spt', 'atharva_theme_base'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/assets.xml',
        'views/custom_referesh_searchbar_assets.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}