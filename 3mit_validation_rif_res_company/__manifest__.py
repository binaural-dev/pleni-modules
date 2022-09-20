# -*- coding: UTF-8 -*-

{
    "name": "Validaciones RIF res.company-res.partner",
    "version": "1.1",
    'category': 'Accounting',
    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'summary': """
        Modifica y realiza validaciones al nif-vat-rif.""",
    'description': """
        * Modifica campo y realiza validaciones al vat(nif) y al email:
            * De la compañia.
            * Del cliente-proveedor.
        Colaborador: Kleiver Pérez.""",
    'depends' : ["base","base_vat","3mit_validation_res_partner", '3mit_grupo_localizacion'],
    "data": [
        'security/ir.model.access.csv',
        'views/3mit_validation_res_company_rif.xml',
	    'views/3mit_validation_res_partner.xml',
             ],
    'installable': True,
}
