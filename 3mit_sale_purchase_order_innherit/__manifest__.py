# coding: utf-8
###########################################################################
{
    "name": "Correcciones ventas y compras; rif, tipo de documento y Documento de Identidad",
    "version": "1.0",
    "author": "Localizacion Venezolana",
    "colaborador":"Maria Carreño",
    "depends": [
        "sale_management",
        "purchase",
        "base",
        "base_vat",
        "3mit_validation_res_partner",
        "3mit_validation_rif_res_company",
        '3mit_grupo_localizacion'
    ],
    "data": [
        'views/sale_order_innherit.xml',
        'views/purchase_order_innherit.xml',
    ],
    'active': True,
    'application': True,
}
