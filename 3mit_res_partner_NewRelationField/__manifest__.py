# -*- coding: utf-8 -*-
{
    'name': "Campo Relacion con Nosotros",

    'summary': """
        Se agrega un campo Relacion con Nosotros para elegir si un contacto es proveedor o cliente
        """,

    'description': """
    Se agrega un campo Selection llamado Relacion con Nosotros en el modelo res_partner para elegir 
    si un contacto es proveedor o cliente
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','3mit_validation_rif_res_company'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
