# -*- coding: utf-8 -*-
{
    'name': "Cambio del tamaño de los productos E-Commerce",

    'summary': """
        Cambio del tamaño de los productos E-Commerce para que entren 4 en la vista de celular
        """,

    'description': """
    Cambio del tamaño de los productos E-Commerce para que entren 4 en la vista de celular mediante media query
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Website/Products',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product','website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "templates/template.xml",
        "templates/assets.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
