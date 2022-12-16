# -*- coding: utf-8 -*-
{
    'name': "pleni_shop",
    'author': "Oriana Graterol",
    'website': "https://www.pleni.app",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base', 
        'website_sale', 
        'sale', 
        'web', 
        'website_uom_select_suggetion_spt', 
        'atharva_theme_base',
        'payment', 
        'pleni_custom_fields'
    ],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/assets.xml',
        'views/custom_referesh_searchbar_assets.xml',
        'views/product_template_inherit_view.xml',
        'views/payments.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'post_init_hook': 'get_most_sold_products',
}