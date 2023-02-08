# -*- coding: utf-8 -*-
{
    'name': 'Pleni Auth API Key',
    'summary': """
        Authenticate http request from an API Key""",
    'version': '0.1.0',
    'category': 'Uncategorized',
    'license': 'GPL-3',
    'author': 'Manuel Escalante',
    'website': 'https://pleni.app',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/auth_api_key.xml'
    ]
}
