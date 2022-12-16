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

    'depends': ['base', 'sale', 'account', 'website', '3mit_so_auto_payment_method', '3mit_so_client_notes'],

    'data': [
        'view/view.xml',
        # 'view/sale_order_inherit.xml',
        'report/report_sale_order.xml'
    ]

}
