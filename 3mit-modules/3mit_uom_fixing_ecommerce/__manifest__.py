# -*- coding: utf-8 -*-
{
    'name': "UOM Fix Ecommerce",

    'summary': """
        Formulario de registro ecommerce.""",

    'description': """
        * Añade nuevos campos para registro desde el ecommerce.
        \nElaborado por: Kleiver Pérez - Carlos Marquez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Ecommerce',
    'version': '1.1.2',

    'depends': ['base', 'sale', 'web', 'website_sale', 'website_uom_select_suggetion_spt', 'atharva_theme_base'],

    'data': [
        'views/assets.xml',
        'views/add_qty_input_inherit.xml'
    ],

}
