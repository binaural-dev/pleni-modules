# -*- coding: utf-8 -*-
{
    'name': "Mejora en la UX del Usuario en el E-Commerce",

    'summary': """
        Mejora en la UX del Usuario en el E-Commerce, se cambio una etiqueta y se agrego una columna
        """,

    'description': """
    Mejora en la UX del Usuario en el E-Commerce, se cambio la etiqueta deprecio por "Precio Unitario" y se agrego una columna llamada "Subtotal".
    Colaborador: Ricardo Sanchez
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Website/Payment',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product','website_sale', 'website_uom_select_suggetion_spt'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "templates/template.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
