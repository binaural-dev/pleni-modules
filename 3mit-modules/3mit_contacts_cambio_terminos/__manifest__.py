# -*- coding: utf-8 -*-
{
    'name': "Cambio de termino en Contactos",

    'summary': """
        Cambia el terminos Móvil en Contactos
        """,

    'description': """
        *Cambia el termino "Móvil" por "Teléfono Móvil"
        *IMPORTANTE: para visualizar los cambios se debe desinstalar y volver a instalar el modulo
        Colaborador: Ricardo Sanchez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",

    'category': 'contacts',
    'version': '1.0',

    'depends': ['base','contacts'],
    'data': [
    ],
    'demo': [
    ],
    'instalable': True,
    'post_init_hook': 'cambio_terminos',
    'uninstall_hook': 'revertir_cambios',
}
