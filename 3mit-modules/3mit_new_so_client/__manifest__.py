# -*- coding: utf-8 -*-
{
    'name': "First SO customer",

    'summary': """
        Verifica si es la primera orden del cliente.""",

    'description': """
        * Agrega booleano en la orden de compra para verificar si es su primera compra.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Sales',
    'version': '1.1.2',

    'depends': ['base', 'sale_management'],

    'data': [
            'views/sale_order_inherit.xml'
        ],

}
