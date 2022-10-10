# -*- coding: utf-8 -*-
{
    'name': "Custom Signup ecommere",

    'summary': """
        Formulario de registro ecommerce.""",

    'description': """
        * Añade nuevos campos para registro desde el ecommerce.
        \nElaborado por: Kleiver Pérez - Carlos Marquez.
        \nCoraborador: Ricardo Sanchez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Ecommerce',
    'version': '1.2.1',

    'depends': ['base', 'auth_signup', 'pleni_custom_fields'],

    'data': [
        'views/custom_signup_templates.xml',
        'views/custom_signup_assets.xml',
        'views/custom_my_details_portal.xml'
    ],

}
