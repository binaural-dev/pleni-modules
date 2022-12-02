# coding: utf-8
###########################################################################

##############################################################################
{
    "name": "Calculo de precio $ de los productos y en la ordern de venta",
    "version": "1.0.1",
    "author": "3mit",
    "license": "AGPL-3",
    "category": "ventas",
    #"website": "",
    "colaborador":"Maria Carreño",
    "depends": [
        "sale",
        "base",
        "base_vat",
        "3mit_rates",
        "product",
        '3mit_field_new_rate_purchase_order',
        '3mit_base_withholdings',
        '3mit_grupo_localizacion'
    ],
    'demo': [
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/sale_order_innherit_compute_rate.xml'
    ],
    'test': [

    ],
    "installable": True,
    'application': True,
}