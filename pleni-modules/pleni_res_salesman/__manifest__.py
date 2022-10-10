{
    'name': "Pleni - Resource Salesman",
    'version': '0.1.5',
    'category': 'Uncategorized',
    'license': 'GPL-3',
    'author': "Manuel Escalante",
    'website': "https://pleni.app",
    'depends': [
        'base',
        'sale',
        '3mit_ve_dpt'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/salesman_security.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/res_salesman_view.xml',
    ]
}
