# -*- coding: utf-8 -*-
{
    'name': "Contacts custom fields",

    'summary': """
        Añade campos al res.partner.""",

    'description': """
        1.1.2: Añade distintos campos tipo char al res.partner.
        1.1.3: Se movieron algunos campos y se editaron etiquetas.
        1.1.4: Se añadió nuevo campo para guardar la data de la Urbanización/Zona en el res.partner.
        1.1.5: Añadido modelo para guardar la información de 'Cómo llegó a nosotros' y 'Zona/Urbanización'.
        1.1.6: Añadido menuitems para visualizar registros de los campos 'Cómo llegó a nosotros' y 'Zona/Urbanización'.
        
        \nElaborado por: Kleiver Pérez, Ricardo Sánchez.
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Contacts',
    'version': '1.1.6',

    'depends': ['base', 'contacts', '3mit_validation_rif_res_company'],

    'data': [
        'security/ir.model.access.csv',
        'data/how_find_us_data.xml',
        'views/how_find_us_views.xml',
        'views/urbanization_area_views.xml',
        'views/res_partner_inherit.xml',
        'views/menu_views.xml',
    ],
}
