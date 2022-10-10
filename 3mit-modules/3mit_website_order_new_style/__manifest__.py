# -*- coding: utf-8 -*-
{
    'name': "Sale Orders-Pay Methods Data",

    'summary': """
        Métodos de pago para las ordenes de pago.""",

    'description': """
        1.1.1: * Adición de una pestaña de mensajes en los diarios contables para colocar los datos para realizar el pago.
               * Adición de los datos del pago al imprimir la orden de venta.
        2.0:   Se cambio el modelo de los metodos de pago de account.journal a payment.acquirer
        \nElaborado por: Carlos Márquez, Ricardo Sanchez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Inventory',
    'version': '2.0',

    'depends': ['base', 'website', 'portal', 'payment', 'sale'],

    'data': [
        "template/templates.xml",
        "assets/assets.xml"
    ]

}
