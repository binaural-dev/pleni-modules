# -*- coding: utf-8 -*-
{
    'name': "Cambio de Estilo Reporte Compras",

    'summary': """
        Cambio de Estilo Reporte Compras.""",

    'description': """
        1.0: Cambio de Estilo Reporte Compras
        \nElaborado por: Ricardo Sanchez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Purchase',
    'version': '1.0',

    'depends': ['base', 'purchase', 'web', 'purchase_stock'],

    'data': [
        # 'view/sale_order_inherit.xml',
        'report/report_purchase.xml',
        'report/report_style_address.xml'
    ]

}
