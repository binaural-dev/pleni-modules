# -*- coding: utf-8 -*-
{
    'name': "SO cancellation reasons",

    'summary': """
        Razones de cancelación y tipo de cancelación.""",

    'description': """
        * Permite añadir motivos de cancelación y sus tipos en las ordenes de ventas.
        * Vista para la pestaña "Otra información".
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
