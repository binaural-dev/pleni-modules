# -*- coding: utf-8 -*-
{
    'name': "Delete P.U. Budgets",

    'summary': """
        Elimina presupuestos del Public User luego de 24 horas.""",

    'description': """
        * Verifica y elimina los presupuestos creados por el public user luego de transcurridas 24 horas.
        * Crea acción planificada para la eliminación de los mismos.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Products',
    'version': '1.1.2',

    'depends': ['base', 'sale', 'purchase', 'stock', 'product'],

    'data': [
        'views/product_template_inherit.xml'
    ], 
}
