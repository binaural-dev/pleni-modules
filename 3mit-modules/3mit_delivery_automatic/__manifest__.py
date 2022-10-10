# -*- coding: utf-8 -*-
{
    'name': "Automatic delivery",

    'summary': """
        Verifica montos menores a $30 en ordenes de venta y añade su delivery.""",

    'description': """
        * Automatización para los deliveries.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Sales',
    'version': '1.1.2',

    'depends': ['base', 'sale_management', 'delivery'],

    'data': [
        'views/sale_order_inherit_view.xml',
    ],

}
