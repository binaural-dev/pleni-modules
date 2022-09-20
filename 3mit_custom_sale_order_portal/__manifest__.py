# -*- coding: utf-8 -*-
{
    'name': "Custom Sale Order Portal",

    'summary': """
        Changes in the sale order portal of the website.""",

    'description': """
        * Add a new column with the status of the order.
        \nElaborado por: Carlos Marquez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Portal',
    'version': '1.1.2',

    'depends': ['base', 'sale'],

    'data': [
        'templates/custom_portal_my_orders.xml'
    ],

}
