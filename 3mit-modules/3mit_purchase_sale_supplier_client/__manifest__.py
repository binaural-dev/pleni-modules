# -*- coding: utf-8 -*-
{
    'name': "Dominio Cliente Proveedor",

    'summary': """
        Dominio en compra y venta para especificacion de proveedor 
        """,

    'description': """
    Colocar un dominio para que alcrear un pedido de venta solo aparezcan clientes y al crear una orden decompra solo aparezcan proveedores
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Contacts, Purchase, Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','purchase','sale','3mit_res_partner_NewRelationField'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
