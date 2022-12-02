# -*- coding: utf-8 -*-
{
    'name': "Automatic payment method",

    'summary': """
        Obtiene automáticamente el diario asociado al método de pago elegido.""",

    'description': """
        * Automatiza la obtención del diario según el método de pago.
        * Campo en la orden de venta para guardar el diario.
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
