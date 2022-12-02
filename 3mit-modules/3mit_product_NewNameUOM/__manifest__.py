# -*- coding: utf-8 -*-
{
    'name': "Productos UOM",

    'summary': """
        Cambio de etiqueta al campo "product_uom_ids"
        """,

    'description': """
    Cambio de etiqueta al campo "product_uom_ids"
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Product',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product','website_uom_select_suggetion_spt'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
