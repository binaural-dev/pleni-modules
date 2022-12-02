# -*- coding: utf-8 -*-
{
    'name': "Hide Purchase Orders from Ecommerce",

    'summary': """
        Oculta los pedidos de compra del ecommerce.""",

    'description': """
        * Oculta el div para los pedidos de compra en el portal.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Ecommerce',
    'version': '1.1.2',

    'depends': ['base', 'web', 'portal', 'purchase', 'sale'],

    'data': [
        'views/hide_po_assets.xml',
    ],

}
