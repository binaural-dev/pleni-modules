# -*- coding: utf-8 -*-
{
    'name': "Personalizacion de Campos en Pedidos",

    'summary': """
        Traslado, creacion y personalizacion de campos en la vista de pedidos en ventas
        """,

    'description': """
    1.0: Traslado, creacion y personalizacion de campos en el modelo sale.order
    1.1: Se le agrego una condicion if ya que daba error al crear una venta desde 0
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Sale',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
