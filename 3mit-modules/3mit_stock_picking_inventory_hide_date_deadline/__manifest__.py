# -*- coding: utf-8 -*-
{
    'name': "Ocultar fecha limite en inventario",

    'summary': """
        Ocultar el campo fecha limite en las transferencias de inventario
        """,

    'description': """
    1.0: Ocultar el campo fecha limite (date_deadline) en la ista principalde transferencias en inventario
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Inventario',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
