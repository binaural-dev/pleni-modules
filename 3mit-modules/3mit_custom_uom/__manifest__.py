# -*- coding: utf-8 -*-
{
    'name': "Custom UOM",

    'summary': """
        UOM custom para Ordenes de compra y venta.""",

    'description': """
        * Solamente permite obtener el uom definido en la plantilla del producto.
        * Dominios custom para ordenes de compra y venta para el uom del producto.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Inventory',
    'version': '1.1.4',

    'depends': ['base', 'sale_management', 'purchase', 'stock', 'website_uom_select_suggetion_spt'],

    'data': [
        'views/sale_order_inherit_view.xml',
        'views/purchase_order_inherit_view.xml',
    ],
}

