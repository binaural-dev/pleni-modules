# -*- coding: utf-8 -*-
{
    "name": "Localización Venezolana: Municipios y Parroquias",
    "version": "0.1",
    "author": "3MIT",
    'website': "https://www.3mit.dev/",
    "category": "Accounting",
    "description":
        """
Localización Venezolana: Municipios y Parroquias
================================================

Basado en información del INE del año 2013, añade los campos de municipio y parroquia en el modelo `res.partner` de
manera que queden disponibles en todos los campos de dirección en modelos derivados como `res.users` o `res.company`.
     """,
    "depends": ['base', '3mit_base_withholdings', '3mit_grupo_localizacion'],
    "data": [
        'security/ir.model.access.csv',
        'data/res.country.state.xml',
        'data/res.country.state.municipality.xml',
        'data/res.country.state.municipality.parish.xml',
        'views/res_company_views.xml',
        'views/3mit_ve_dpt_view.xml',
        'views/res_partner.xml',
    ],
    "installable": True
}
