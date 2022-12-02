# -*- coding: UTF-8 -*-

{
    "name": "Validaciones res.partner",
    "version": "1.1",
    'category' : 'Accounting',
    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'summary': """
        Validaciones y adición de campos sobre el partner cliente-proveedor.""",
    'description' : """
        Agrega el tipo de persona, y coloca el Documento de Identidad segun el tipo de persona y sus respectivos atributos.\n
        Colaborador: Kleiver Pérez.""",
    'depends' : ["base","base_vat", "3mit_grupo_localizacion"],
    "data": [
        'security/ir.model.access.csv',
        'views/res_partner_people_type.xml',
        'views/docum_ident_res_partner.xml',
             ],
    'installable': True,
}
