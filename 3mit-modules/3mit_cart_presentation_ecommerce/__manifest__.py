# -*- coding: utf-8 -*-
{
    'name': "Products most sold",

    'summary': """
        Modificación productos más vendidos ecommerce.""",

    'description': """
        * Modifica el renderizado del '/shop' para obtener los más vendidos y ordenarlos.
        \nElaborado por: Kleiver Pérez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'E-commerce',
    'version': '1.1.1',

    'depends': ['base', 'website_sale', 'sale_management', 'atharva_theme_base', 'website_uom_select_suggetion_spt'],

    'data': ['views/product_template_inherit_view.xml'],

    'post_init_hook': 'get_most_sold_products',

}
