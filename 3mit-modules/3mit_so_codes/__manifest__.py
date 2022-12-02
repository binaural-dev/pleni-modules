# -*- coding: utf-8 -*-
{
    'name': "SO codes",

    'summary': """
        Códigos para ordenes de venta.""",

    'description': """
        * Permite modificar la secuencia en las ordenes de ventas por usuario.
        * Configuración de prefijos y secuencias para usuarios.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Sales',
    'version': '1.1.2',

    'depends': ['base', 'contacts', 'sale_management'],

    'data': [
            'views/res_users_inherit.xml'
        ],

}
