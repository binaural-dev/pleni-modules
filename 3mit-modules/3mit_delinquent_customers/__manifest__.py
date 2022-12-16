# -*- coding: utf-8 -*-
{
    'name': "3mit Delinquent Customers",
    'summary': """ Verificacion de clientes morosos para ventas en el sistema.""",
    'description': """ Verificacion del numero de factura vencidas del cliente para condicionar sus nuevos pedidos.
    Tambien funciona para el ecommerce.
    Project: Los gochos
    Colaborador: Carlos Marquez """,
    'author': "3MIT",
    'website': "https://3mit.dev",
    'category': 'Sales',
    'version': '1.0.0',
    "depends": [
        "purchase",
        "sale",
        "website_sale"
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/warning_wizard.xml',
        'templates/delinquent_customer_error.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'application': True,
}
