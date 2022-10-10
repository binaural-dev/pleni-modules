# -*- coding: utf-8 -*-
{
    'name': "Reporte Factura Venta",

    'summary': """
        Reestructuracion completa del reporte de Factura de Venta""",

    'description': """
        1.0: Reestructuracion completa del reporte de Factura de Venta:
            * ELIMINE: Fecha de Vencimiento, Origen y Por favor utilice la siguiente referencia al realizar su pago: INV/2022/06/0009.
            * CAMBIE: Fecha de Factura por Fecha Programada de entrga y La direccion por los datos del cliente.
            * AGREGUE: Las notas del cliente, el metodo de pago y los datos de pago 
        \nElaborado por: Ricardo Sanchez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Account',
    'version': '1.0',

    'depends': ['base', 'sale', 'account', 'website', '3mit_so_client_notes'],

    'data': [
        # 'view/sale_order_inherit.xml',
        'report/report_account_move_invoice.xml',
        'report/report_delivery_slip.xml'
    ]

}
