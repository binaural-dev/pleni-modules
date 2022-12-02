# coding: utf-8

{
    "name": "Validaciones facturación",
    "version": "1.1",
    'author': "3MIT",
    'website': "https://www.3mit.dev/",
    "license": "AGPL-3",
    "category": "Accounting",
    'summary': """
        Añade números de control automáticos en la factura a clientes-proveedores.""",
    'description': """
        * Realiza validaciones y correciones en la facturación.
        * Añade números de control automáticos para:
            * Clientes.
            * Proveedores.
        Colaborador: Maria Carreño, Kleiver Pérez.""",
    "depends": [
        "account",
        "base",
        "base_vat",
        "3mit_validation_res_partner",
        "3mit_validation_rif_res_company",
        '3mit_grupo_localizacion'
    ],
    "data": [
        'security/ir.model.access.csv',
        'view/invoice_view.xml',
    ],
    'installable': True,
}
