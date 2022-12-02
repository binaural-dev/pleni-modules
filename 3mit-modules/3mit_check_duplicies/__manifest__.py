# -*- coding: utf-8 -*-
{
    'name': "Action duplicar de factura proveedor",

    'summary': """
        Modifica el botón de duplicar para las facturas del proveedor
        """,

    'description': """
        Realiza modificaciones al botón de duplicar factura:\n
            * Modifica el status de la factura duplicada.
            * Evita generar documento de retención de ingresos.
            * Evita generar el número de control por default.
            * Evita que se cree el número de factura de proveedor por default.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Account',
    'version': '1.1',

    'depends': ['base', 'account', '3mit_withholding_islr'],

    'data': [

    ],
    'demo': [

    ],
}
