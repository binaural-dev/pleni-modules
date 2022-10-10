# -*- coding: utf-8 -*-
{
    'name': "Campos Obligatorios en Contacto",

    'summary': """
        Colocar como requerido campos en la ficha de contacto
        """,

    'description': """
    1.1: Colocarcomo requeridos campos en la ficha de contacto (Nombre del cliente, Razon social, 
         Tipo de persona, CI/RIF, Direccion, Zona/Urbanizacion, Telefono Movil, Correo electronico, 
         Categotia del cliente, Plus code, Requiere factura fiscal, vendedor y como llego a nosotros)
         Colaborador: Ricardo Sanchez
    1.2: Se oculto el campo IVA(vat) 
    """,

    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    'category': 'Contacts',
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','3mit_validation_rif_res_company','3mit_ve_dpt','pleni_custom_fields'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "views/view.xml"
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
