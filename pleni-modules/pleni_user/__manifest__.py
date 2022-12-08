# -*- coding: utf-8 -*-
{
    'name': "pleni_user",
    'author': "Oriana Graterol",
    'website': "https://www.pleni.app",
    'category': 'Contacts',
    'version': '0.1',
    'depends' : [
        "base",
        'contacts',
        "base_vat",
        "3mit_validation_res_partner",
        '3mit_validation_rif_res_company', 
        'pleni_custom_fields',
        '3mit_grupo_localizacion',
        'auth_signup'
    ],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/validation_res_partner.xml',
        'views/validation_res_company_rif.xml',
        'views/custom_signup_templates.xml',
        'views/custom_signup_assets.xml',
        'views/custom_my_details_portal.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}