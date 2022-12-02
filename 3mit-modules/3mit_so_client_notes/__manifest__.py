# -*- coding: utf-8 -*-
{
        'name': "SO client notes",

    'summary': """
        Notas del cliente en ordenes de venta.""",

    'description': """
        * Campo para notas del cliente en ordenes de venta.
        * Adición de campo en reporte impreso.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Sales',
    'version': '1.1.2',

    'depends': ['base', 'sale_management'],

    'data': [
        'views/sale_order_inherit.xml',
        'reports/sale_order_report_inherit.xml',
    ],

}
